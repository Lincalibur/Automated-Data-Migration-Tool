import io

import main


def client():
    main.app.config['TESTING'] = True
    return main.app.test_client()


def test_index_renders_conversion_options():
    response = client().get('/')
    assert response.status_code == 200
    assert b'Automated Data Migration Tool' in response.data


def test_upload_requires_a_file():
    response = client().post('/upload', data={})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'No file provided'


def test_upload_then_convert_pdf_to_word():
    from pypdf import PdfWriter

    buffer = io.BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.write(buffer)
    buffer.seek(0)

    test_app = client()
    upload_response = test_app.post(
        '/upload', data={'file': (buffer, 'sample.pdf')}, content_type='multipart/form-data'
    )
    assert upload_response.status_code == 200
    file_path = upload_response.get_json()['file_path']

    convert_response = test_app.post('/convert', json={'file_path': file_path, 'convert_to': 'pdf_to_word'})
    assert convert_response.status_code == 200
    assert convert_response.get_json()['destination_file'].endswith('.docx')


def test_convert_rejects_unknown_type():
    response = client().post('/convert', json={'file_path': 'x.pdf', 'convert_to': 'nonsense'})
    assert response.status_code == 400
