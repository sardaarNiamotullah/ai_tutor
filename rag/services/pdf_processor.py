import fitz  # PyMuPDF
from ..embeddings.chunker import chunk_text
from ..embeddings.embedder import generate_embeddings

def process_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    cleaned = " ".join(text.split())  # Remove newlines, extra spaces
    chunks = chunk_text(cleaned)
    embeddings = generate_embeddings(chunks)

    return chunks # or embeddings if you prefer
