def chunk_text(text: str, chunk_size: int = 6000):
    """
    Split long text into chunks for LLM processing.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end

    return chunks