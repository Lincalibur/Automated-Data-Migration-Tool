from docx import Document
from PyPDF2 import PdfReader

def pdf_to_word_converter(pdf_file_path, word_file_path):
    pdf_reader = PdfReader(pdf_file_path)
    doc = Document()

    for page in pdf_reader.pages:
        text = page.extract_text()
        doc.add_paragraph(text)

    doc.save(word_file_path)
    print(f"Converted {pdf_file_path} to {word_file_path}")
