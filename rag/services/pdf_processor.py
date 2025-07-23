import fitz
from ..embeddings.chunker import chunk_text
from ..embeddings.embedder import generate_embeddings
from .preprocessor import clean_text


def process_pdf(file_path):
    doc = fitz.open(file_path)
    raw_text = ""
    for page in doc:
        raw_text += page.get_text()

    cleaned_text, language = clean_text(raw_text)

    # ✅ Pass the detected language to chunk_text
    chunks = chunk_text(cleaned_text, language=language)

    embeddings = generate_embeddings(chunks)

    return chunks
