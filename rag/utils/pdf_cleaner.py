import re
from langdetect import detect  # Lightweight language detection based on character n-grams


def detect_language(text):
    """
    Detects the language of a given text using langdetect.

    Args:
        text (str): Input text.

    Returns:
        str: ISO 639-1 language code (e.g., 'bn', 'en'), or 'unknown' on failure.
    """
    try:
        return detect(text)
    except:
        return "unknown"  # Fallback in case detection fails (e.g., very short or ambiguous text)


def clean_text(text):
    """
    Cleans the input text based on its detected language.

    - For Bangla ('bn'):
        - Removes Bangla digits (০-৯)
        - Keeps only Bangla characters (Unicode range \u0980–\u09FF)
        - Preserves common Bangla punctuation (e.g., ।, !, ?)
    - For English or other languages:
        - Keeps letters, numbers, whitespace, and basic punctuation (., ?, !)

    Args:
        text (str): Raw extracted text from a PDF.

    Returns:
        Tuple[str, str]:
            - Cleaned text string
            - Detected language code ('bn', 'en', etc.)
    """

    # 🔍 Detect whether the text is in Bangla or another language
    language = detect_language(text)

    if language == "bn":
        # 🧹 Step 1 (Bangla): Remove Bangla digits (০-৯)
        text = re.sub(r"[০-৯]", "", text)

        # 🧹 Step 2 (Bangla): Keep only Bangla letters, whitespace, and punctuation (।!?)
        text = re.sub(r"[^\u0980-\u09FF\s।!?]", "", text)
    else:
        # 🧹 Step 1 (Other): Keep only alphanumeric characters and basic punctuation
        text = re.sub(r"[^a-zA-Z0-9\s.?!]", "", text)

    # 🧼 Normalize whitespace: convert multiple spaces/newlines/tabs to single space
    text = re.sub(r"\s+", " ", text)

    # 🧾 Return the cleaned text and the detected language
    return text.strip(), language