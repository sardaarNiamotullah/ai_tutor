import fitz
import logging
from ..embeddings.chunker import chunk_text
from ..embeddings.embedder import generate_embeddings
from .preprocessor import clean_text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_pdf(file_path):
    doc = fitz.open(file_path)
    raw_text = ""
    for page in doc:
        raw_text += page.get_text()
    
        
    # logger.info(f"Extracted raw text (first 500 chars):\n{raw_text[:500]}...")

    cleaned_text, language = clean_text(raw_text)

    # ✅ Pass the detected language to chunk_text
    chunks = chunk_text(cleaned_text, language=language)

    embeddings = generate_embeddings(chunks)

    return chunks, language
