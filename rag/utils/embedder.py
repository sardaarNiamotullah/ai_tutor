from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def split_into_sentences_bn(text):
    import re
    return [s.strip() for s in re.split(r'[।!?]', text) if s.strip()]

def chunk_text(text, language):
    if language == "bn":
        text = "\n".join(split_into_sentences_bn(text))
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)

def chunk_and_embed(cleaned_text, language):
    chunks = chunk_text(cleaned_text, language)
    embeddings = model.encode(chunks).tolist()
    return chunks, embeddings
