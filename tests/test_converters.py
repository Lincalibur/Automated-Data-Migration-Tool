import pandas as pd
from docx import Document
from pypdf import PdfWriter

from converters.pdf_to_word import pdf_to_word_converter
from converters.sql_to_excel import sql_to_excel_converter
from data_sources.database_connector import DatabaseConnector


def test_pdf_to_word_converter_produces_docx(tmp_path):
    pdf_path = tmp_path / 'input.pdf'
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    with open(pdf_path, 'wb') as f:
        writer.write(f)

    docx_path = tmp_path / 'output.docx'
    pdf_to_word_converter(str(pdf_path), str(docx_path))

    assert docx_path.exists()
    Document(str(docx_path))  # raises if not a valid docx


def test_sql_to_excel_converter_exports_default_table(tmp_path):
    db_path = tmp_path / 'source.db'
    DatabaseConnector(f"sqlite:///{db_path}").write_table(
        'orders', pd.DataFrame({'id': [1, 2], 'total': [9.99, 19.99]})
    )

    excel_path = tmp_path / 'orders.xlsx'
    sql_to_excel_converter(str(db_path), str(excel_path))

    result = pd.read_excel(excel_path)
    assert result['id'].tolist() == [1, 2]
