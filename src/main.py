import os
from flask import Flask, request, jsonify, render_template, send_from_directory

from convertibles import CONVERTIBLES
from etl.extract import DataExtractor
from etl.transform import DataTransformer
from etl.load import DataLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'ui', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'ui', 'static'),
)

UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploaded_files')
OUTPUT_FOLDER = os.path.join(BASE_DIR, '..', 'output_files')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html', conversions=list(CONVERTIBLES.keys()))


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200


@app.route('/convert', methods=['POST'])
def convert_file():
    payload = request.json or {}
    file_path = payload.get('file_path')
    convert_to = payload.get('convert_to')

    if not file_path or not convert_to:
        return jsonify({'error': 'Invalid request'}), 400

    conversion_info = CONVERTIBLES.get(convert_to)
    if not conversion_info:
        return jsonify({'error': 'Conversion type not supported'}), 400

    if not os.path.exists(file_path):
        return jsonify({'error': f'Source file not found: {file_path}'}), 400

    base_name = os.path.splitext(os.path.basename(file_path))[0]
    destination_file_path = os.path.join(OUTPUT_FOLDER, base_name + conversion_info['destination_ext'])

    try:
        conversion_info['converter'](file_path, destination_file_path)
    except Exception as exc:
        return jsonify({'error': f'Conversion failed: {exc}'}), 500

    return jsonify({'message': 'File converted successfully', 'destination_file': destination_file_path}), 200


@app.route('/migrate', methods=['POST'])
def migrate():
    """Run a generic extract -> transform (field mapping) -> load pipeline
    between a file or database source and a file or database destination.

    Expected JSON body:
    {
        "source": {"type": "file", "path": "uploaded_files/customers.csv"},
        "destination": {"type": "database", "connection_string": "sqlite:///output_files/warehouse.db", "table": "customers"},
        "field_map": {"cust_name": "customer_name"}
    }
    """
    payload = request.json or {}
    source = payload.get('source')
    destination = payload.get('destination')
    field_map = payload.get('field_map')

    if not source or not destination:
        return jsonify({'error': 'Both source and destination are required'}), 400

    try:
        data = DataExtractor(source).extract()
        transformed = DataTransformer(field_map=field_map).transform(data)
        DataLoader(destination).load(transformed)
    except Exception as exc:
        return jsonify({'error': f'Migration failed: {exc}'}), 500

    return jsonify({'message': 'Migration completed successfully', 'rows_migrated': len(transformed)}), 200


@app.route('/output_files/<path:filename>')
def download_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
