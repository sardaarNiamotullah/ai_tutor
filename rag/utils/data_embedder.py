from sentence_transformers import SentenceTransformer
from .data_chunker import chunk_text

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def chunk_and_embed(cleaned_text, language):
    chunks = chunk_text(cleaned_text, language)
    embeddings = model.encode(chunks).tolist()
    return chunks, embeddings
