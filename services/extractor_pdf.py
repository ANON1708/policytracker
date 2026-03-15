import requests
import fitz


def extract_pdf_text(url: str) -> str:
    response = requests.get(
        url,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )
    response.raise_for_status()

    pdf_bytes = response.content
    document = fitz.open(stream=pdf_bytes, filetype="pdf")

    pages = []
    for page in document:
        page_text = page.get_text("text")
        if page_text:
            pages.append(page_text.strip())

    return "\n\n".join(pages).strip()