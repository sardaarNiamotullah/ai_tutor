import fitz  # PyMuPDF
import re
from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def clean_text(text):
    language = detect_language(text)
    if language == "bn":
        text = re.sub(r"[০-৯]", "", text)
        text = re.sub(r"[^\u0980-\u09FF\s।!?]", "", text)
    else:
        text = re.sub(r"[^a-zA-Z0-9\s.?!]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(), language

def read_and_clean_pdf(file_path):
    doc = fitz.open(file_path)
    raw_text = "\n".join([page.get_text() for page in doc])
    cleaned, lang = clean_text(raw_text)
    print(f"[Reader] 🧼 Cleaned text (first 500 chars): {cleaned[:500]}")
    return cleaned, lang
