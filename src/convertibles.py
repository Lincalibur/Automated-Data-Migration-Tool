# src/convertibles.py
from converters.pdf_to_word import pdf_to_word_converter
from converters.sql_to_excel import sql_to_excel_converter

CONVERTIBLES = {
    'pdf_to_word': {
        'source_ext': '.pdf',
        'destination_ext': '.docx',
        'converter': pdf_to_word_converter,
    },
    'sql_to_excel': {
        'source_ext': '.db',
        'destination_ext': '.xlsx',
        'converter': sql_to_excel_converter,
    },
    # Add more predefined convertibles here
}
