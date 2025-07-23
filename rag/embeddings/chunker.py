from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text, language="en"):
    if language == "bn":
        from ..services.preprocessor import split_into_sentences_bn
        sentences = split_into_sentences_bn(text)
        text = "\n".join(sentences)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_text(text)

