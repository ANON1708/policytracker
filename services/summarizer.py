import re
import requests
from services.chunker import chunk_text

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"


def query_model(prompt: str, num_predict: int = 400) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": num_predict,
            },
        },
        timeout=180,
    )

    response.raise_for_status()
    data = response.json()

    if "response" not in data:
        raise Exception(f"Unexpected Ollama response: {data}")

    return data["response"].strip()


def split_into_sentences(text: str) -> list[str]:
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def normalize_bullets(text: str, fallback_source_text: str) -> list[str]:
    """
    Try to turn model output into up to 5 bullets.
    If the model returns a paragraph instead of bullets, convert sentences into bullets.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    bullets = []
    for line in lines:
        cleaned = re.sub(r"^[\-\*\•\d\.\)\s]+", "", line).strip()
        if cleaned:
            bullets.append(cleaned)

    # If model returned one paragraph, convert it to bullets by sentence
    if len(bullets) <= 1:
        sentence_source = text if text else fallback_source_text
        bullets = split_into_sentences(sentence_source)

    return bullets[:5]


def generate_research_summary(text: str) -> list[str]:
    chunks = chunk_text(text, 3000)
    first_chunk = chunks[0] if chunks else text

    prompt = f"""
You are an expert policy analyst.

Summarize the following AI policy or regulation content into EXACTLY 5 concise bullet points.

Rules:
- each bullet should be one sentence
- each bullet should be specific
- return only the bullet points
- start each bullet with "- "

TEXT:
{first_chunk}
"""

    result = query_model(prompt, num_predict=250)
    bullets = normalize_bullets(result, first_chunk)

    # Fallback if still empty
    if not bullets:
        bullets = split_into_sentences(first_chunk)[:5]

    return bullets


def generate_medium_draft(text: str, title: str) -> str:
    chunks = chunk_text(text, 3000)
    first_chunk = chunks[0] if chunks else text

    prompt = f"""
You are a clear, concise Medium writer.

Write a short Medium-style article of around 400-500 words.

Title: {title}

Requirements:
- explain the policy in simple language
- sound researched but readable
- use short paragraphs
- end with a line starting with "Source:"

TEXT:
{first_chunk}
"""

    result = query_model(prompt, num_predict=700)

    if not result:
        return f"{title}\n\nNo Medium draft could be generated.\n\nSource: {title}"

    return result.strip()


def generate_relevant_excerpts(text: str) -> list[str]:
    chunks = chunk_text(text, 3000)
    first_chunk = chunks[0] if chunks else text

    prompt = f"""
Extract exactly 3 important excerpts from the following text.

Rules:
- each excerpt should be 1-2 sentences
- each excerpt should be on a new line
- return only the excerpts
- do not add numbering or commentary

TEXT:
{first_chunk}
"""

    result = query_model(prompt, num_predict=220)

    lines = [line.strip() for line in result.split("\n") if line.strip()]
    cleaned = [re.sub(r"^[\-\*\•\d\.\)\s]+", "", line).strip() for line in lines if line.strip()]

    if len(cleaned) < 3:
        cleaned = split_into_sentences(first_chunk)[:3]

    return cleaned[:3]


def summarize_text(text: str, title: str = "Untitled Source") -> dict:
    if not text or not text.strip():
        return {
            "summary": ["No text could be extracted from this source."],
            "medium_draft": f"{title}\n\nNo Medium draft could be generated because no source text was available.\n\nSource: {title}",
            "excerpts": [],
        }

    return {
        "summary": generate_research_summary(text),
        "medium_draft": generate_medium_draft(text, title),
        "excerpts": generate_relevant_excerpts(text),
    }