from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def split_into_sentences_bn(text):
    return [s.strip() for s in re.split(r'[।!?]', text) if s.strip()]

def chunk_text(text, language):
    if language == "bn":
        text = "\n".join(split_into_sentences_bn(text))
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_text(text)
