import re
from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def clean_text(text):
    language = detect_language(text)

    if language == "bn":
        # Bangla-specific cleanup
        text = re.sub(r"[০-৯]", "", text)  # Remove Bangla digits
        text = re.sub(r"[^\u0980-\u09FF\s।!?]", "", text)  # Keep dari (।), !, ? for sentence splitting
        text = re.sub(r"\s+", " ", text)
    else:
        # English/general cleanup
        text = re.sub(r"[^a-zA-Z0-9\s.?!]", "", text)
        text = re.sub(r"\s+", " ", text)

    return text.strip(), language

def split_into_sentences_bn(text):
    # Split using Bengali sentence-ending punctuation (। ! ?)
    sentences = re.split(r'[।!?]', text)
    return [s.strip() for s in sentences if s.strip()]
