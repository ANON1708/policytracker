import json
import uuid
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, urlunparse

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_DIR = BASE_DIR / "data" / "sources"


def ensure_sources_dir():
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)


def current_timestamp():
    return datetime.now().isoformat()


def normalize_url(url: str) -> str:
    url = url.strip()
    parsed = urlparse(url)

    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")

    cleaned = parsed._replace(
        scheme=scheme,
        netloc=netloc,
        path=path,
        params="",
        query="",
        fragment=""
    )
    return urlunparse(cleaned)


def create_source(url: str, title: str = "Untitled Source"):
    ensure_sources_dir()

    normalized_url = normalize_url(url)

    for file_path in SOURCES_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = json.load(f)
                if normalize_url(source.get("url", "")) == normalized_url:
                    return {
                        "created": False,
                        "source_id": source.get("id"),
                        "message": "Source already exists"
                    }
        except Exception:
            continue

    source_id = str(uuid.uuid4())
    now = current_timestamp()

    source_data = {
        "id": source_id,
        "url": normalized_url,
        "title": title.strip() if title else "Untitled Source",
        "tags": [],
        "text": "",
        "summary": [],
        "medium_draft": "",
        "excerpts": [],
        "status": "Not summarised yet",
        "created_at": now,
        "last_checked": "",
        "history": []
    }

    file_path = SOURCES_DIR / f"{source_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(source_data, f, indent=2, ensure_ascii=False)

    return {
        "created": True,
        "source_id": source_id,
        "message": "Source added successfully"
    }


def get_all_sources():
    ensure_sources_dir()
    sources = []

    for file_path in SOURCES_DIR.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = json.load(f)
                sources.append(source)
        except Exception:
            continue

    # Always alphabetical by title, fallback to url
    sources.sort(
        key=lambda x: (
            (x.get("title") or "").strip().lower() if (x.get("title") or "").strip() else (x.get("url") or "").lower()
        )
    )
    return sources


def get_source(source_id: str):
    ensure_sources_dir()

    file_path = SOURCES_DIR / f"{source_id}.json"
    if not file_path.exists():
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_source(source_data):
    ensure_sources_dir()

    file_path = SOURCES_DIR / f"{source_data['id']}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(source_data, f, indent=2, ensure_ascii=False)


def delete_source(source_id: str):
    ensure_sources_dir()

    file_path = SOURCES_DIR / f"{source_id}.json"
    if file_path.exists():
        file_path.unlink()
        return True
    return False


def add_history_entry(source_data, event_type: str):
    source_data.setdefault("history", [])
    source_data["history"].append({
        "date": current_timestamp(),
        "type": event_type
    })
    return source_data