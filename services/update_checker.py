import hashlib


def generate_text_hash(text: str) -> str:
    if not text:
        text = ""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def has_text_changed(old_text: str, new_text: str) -> bool:
    old_hash = generate_text_hash(old_text)
    new_hash = generate_text_hash(new_text)
    return old_hash != new_hash


def get_update_status(old_text: str, new_text: str) -> str:
    if has_text_changed(old_text, new_text):
        return "Update detected"
    return "No change detected"