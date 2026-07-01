import os
import json
import anthropic
from backend.qdrant_client import search
from backend.models import QuizQuestion

anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """You generate multiple-choice quiz questions from training document excerpts.
For each question produce exactly one correct answer and exactly three plausible wrong answers.
Respond ONLY with a JSON array. Each element: {"question": "...", "correct_answer": "...", "distractors": ["...", "...", "..."], "source_section": "..."}"""

def generate_quiz(topic: str, num_questions: int = 5) -> list[QuizQuestion]:
    chunks = search(topic, top_k=8)
    context = "\n\n".join(
        f"[Section: {c['section']}]\n{c['text']}" for c in chunks
    )
    user_prompt = f"Generate {num_questions} quiz questions from these excerpts about '{topic}':\n\n{context}"

    message = anthropic_client.messages.create(
        model=MODEL,
        max_tokens=2048,
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
        return []
    return [QuizQuestion(**q) for q in data[:num_questions]]
