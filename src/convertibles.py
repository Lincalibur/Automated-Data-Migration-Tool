# src/convertibles.py

from converters.pdf_to_word import pdf_to_word_converter
from converters.sql_to_excel import sql_to_excel_converter
# Import other conversion functions as needed

CONVERTIBLES = {
    'pdf_to_word': {
        'source_type': 'pdf',
        'destination_type': 'word',
        'converter': pdf_to_word_converter
    },
    'sql_to_excel': {
        'source_type': 'sql',
        'destination_type': 'excel',
        'converter': sql_to_excel_converter
    },
    # Add more predefined convertibles here
}
