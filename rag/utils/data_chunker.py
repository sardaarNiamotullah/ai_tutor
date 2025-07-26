from langchain.text_splitter import RecursiveCharacterTextSplitter
import re


def split_into_sentences_bn(text):
    """
    ✂️ Custom Bangla sentence splitter.

    Bangla sentences typically end with punctuation like:
    - '।' (Dari — Bangla full stop)
    - '!' or '?'

    This function splits the text using those delimiters.

    Args:
        text (str): Bangla text block.

    Returns:
        List[str]: List of sentences after cleaning and trimming.
    """
    return [s.strip() for s in re.split(r'[।!?]', text) if s.strip()]


def chunk_text(text, language):
    """
    🔀 Splits text into overlapping chunks optimized for embedding and retrieval.

    Uses LangChain's RecursiveCharacterTextSplitter to break long texts
    into smaller overlapping segments that preserve sentence boundaries
    and reduce context loss.

    Args:
        text (str): Full cleaned document text.
        language (str): Detected language of the text ('bn', 'en', etc.)

    Returns:
        List[str]: List of text chunks ready for embedding.
    """

    # 🧾 Step 1: Language-specific pre-processing (Bangla needs sentence segmentation first)
    if language == "bn":
        # Break Bangla into separate sentences first
        # This reduces the chance of chunking mid-sentence
        text = "\n".join(split_into_sentences_bn(text))

    # 🧩 Step 2: Initialize the LangChain text splitter
    # - chunk_size=1000: Max characters per chunk
    # - chunk_overlap=200: 200-character overlap to preserve context
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    # 🧠 Step 3: Perform recursive splitting
    # LangChain will try to split by paragraphs, then sentences, then characters
    chunks = splitter.split_text(text)

    return chunks
