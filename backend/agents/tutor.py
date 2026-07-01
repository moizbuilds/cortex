import os
import json
import anthropic
from backend.qdrant_client import search
from backend.models import TutorResponse, Citation

anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You are a corporate training assistant. Answer questions ONLY using the provided document excerpts.
If the answer is not in the excerpts, say "I cannot find that in the training materials."
Always respond in valid JSON matching exactly: {"answer": "...", "citations": [{"section": "...", "page": N}], "confidence": 0.0-1.0}"""

def answer_question(question: str) -> TutorResponse:
    chunks = search(question, top_k=5)
    context = "\n\n".join(
        f"[Section: {c['section']}, Page: {c['page']}]\n{c['text']}" for c in chunks
    )
    user_prompt = f"Document excerpts:\n{context}\n\nQuestion: {question}"

    message = anthropic_client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    raw = message.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return TutorResponse(answer="I encountered an error processing the response.", citations=[], confidence=0.0)
    return TutorResponse(
        answer=data["answer"],
        citations=[Citation(**c) for c in data.get("citations", [])],
        confidence=data.get("confidence", 0.5),
    )
