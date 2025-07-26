import fitz  # PyMuPDF
from .pdf_cleaner import clean_text  # Handles language detection and text normalization


def read_and_clean_pdf(file_path):
    """
    📄 Reads a PDF file from the given path, extracts all text,
    and cleans it for downstream processing (chunking, embedding).

    Args:
        file_path (str): Absolute path to the PDF file on disk.

    Returns:
        Tuple[str, str]:
            - cleaned: A cleaned version of the full PDF text.
            - lang: Detected language code (e.g., 'bn' for Bangla, 'en' for English).
    """

    # ---------------------------------------------------------------
    # 📥 Step 1: Open the PDF using PyMuPDF (fitz)
    # ---------------------------------------------------------------
    doc = fitz.open(file_path)

    # ---------------------------------------------------------------
    # 📃 Step 2: Extract raw text from all pages
    # - get_text() is reliable and supports Unicode
    # - Join all page texts with newline separation
    # ---------------------------------------------------------------
    raw_text = "\n".join([page.get_text() for page in doc])

    # ---------------------------------------------------------------
    # 🧼 Step 3: Clean the raw text using our custom cleaner
    # - Removes special characters, normalizes Bangla or English
    # - Detects and returns the text language
    # ---------------------------------------------------------------
    cleaned, lang = clean_text(raw_text)

    # ---------------------------------------------------------------
    # ✅ Step 4: Return the cleaned text and its language
    # ---------------------------------------------------------------
    return cleaned, lang