from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2") # Supports English, Bangla, and 50+ other languages

def generate_embeddings(chunks):
    return model.encode(chunks).tolist()  # Return as list of vectors
