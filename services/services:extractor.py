from services.extractor_web import extract_webpage_text
from services.extractor_pdf import extract_pdf_text


def is_pdf_url(url: str) -> bool:
    return url.lower().endswith(".pdf")


def extract_source_text(url: str) -> str:
    if is_pdf_url(url):
        return extract_pdf_text(url)
    return extract_webpage_text(url)