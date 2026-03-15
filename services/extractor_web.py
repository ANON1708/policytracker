import requests
import trafilatura
from bs4 import BeautifulSoup
from trafilatura.metadata import extract_metadata


def extract_webpage_content(url: str) -> dict:
    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        },
    )
    response.raise_for_status()

    html = response.text

    extracted_text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=True,
        no_fallback=False,
    )

    soup = BeautifulSoup(html, "html.parser")
    title = None

    # 1. Trafilatura metadata title
    metadata = extract_metadata(html)
    if metadata and getattr(metadata, "title", None):
        title = metadata.title.strip()

    # 2. Open Graph title
    if not title:
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            title = og_title.get("content").strip()

    # 3. HTML <title>
    if not title and soup.title and soup.title.string:
        title = soup.title.string.strip()

    # 4. First H1
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)

    # 5. Fallback from URL
    if not title:
        title = url.replace("https://", "").replace("http://", "").split("/")[0]

    return {
        "title": title,
        "text": extracted_text.strip() if extracted_text else "",
    }


def extract_webpage_text(url: str) -> str:
    content = extract_webpage_content(url)
    return content["text"]