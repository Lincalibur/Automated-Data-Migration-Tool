import os
from flask import Flask, request, jsonify
from convertibles import CONVERTIBLES

app = Flask(__name__)
UPLOAD_FOLDER = 'uploaded_files'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200

@app.route('/convert', methods=['POST'])
def convert_file():
    file_path = request.json.get('file_path')
    convert_to = request.json.get('convert_to')

    if not file_path or not convert_to:
        return jsonify({'error': 'Invalid request'}), 400

    conversion_info = CONVERTIBLES.get(convert_to)

    if not conversion_info:
        return jsonify({'error': 'Conversion type not supported'}), 400

    # Call the appropriate conversion function
    destination_file_path = file_path.replace(conversion_info['source_type'], conversion_info['destination_type'])
    conversion_info['converter'](file_path, destination_file_path)

    return jsonify({'message': 'File converted successfully', 'destination_file': destination_file_path}), 200

if __name__ == "__main__":
    app.run(debug=True)
