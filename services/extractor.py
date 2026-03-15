from services.extractor_web import extract_webpage_content
from services.extractor_pdf import extract_pdf_text


def is_pdf_url(url: str) -> bool:
    return url.lower().endswith(".pdf")


def extract_source_content(url: str) -> dict:
    if is_pdf_url(url):
        return {
            "title": "PDF Source",
            "text": extract_pdf_text(url),
        }

    return extract_webpage_content(url)


def extract_source_text(url: str) -> str:
    return extract_source_content(url)["text"]