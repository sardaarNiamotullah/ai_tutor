import fitz  # PyMuPDF
from .pdf_cleaner import clean_text

def read_and_clean_pdf(file_path):
    doc = fitz.open(file_path)
    raw_text = "\n".join([page.get_text() for page in doc])
    cleaned, lang = clean_text(raw_text)
    print(f"[Reader] 🧼 Cleaned text (first 500 chars): {cleaned[:500]}")
    return cleaned, lang
