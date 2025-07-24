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
        text = re.sub(r"[০-৯]", "", text)
        text = re.sub(r"[^\u0980-\u09FF\s।!?]", "", text)
    else:
        text = re.sub(r"[^a-zA-Z0-9\s.?!]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(), language
