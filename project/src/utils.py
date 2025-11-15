def clean_text(text: str) -> str:
    new = text.replace("\t", " ").replace("\n", " ")
    cleaned = " ".join(new.split())
    return cleaned