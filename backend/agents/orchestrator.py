import re
from backend.agents.tutor import answer_question
from backend.agents.quiz_generator import generate_quiz
from backend.models import OrchestratorResponse

QUIZ_PATTERNS = re.compile(
    r"\b(quiz|test|question|questions|assess|examine)\b", re.IGNORECASE
)

def _classify(user_input: str) -> str:
    if QUIZ_PATTERNS.search(user_input):
        return "quiz"
    return "question"

def _extract_topic(user_input: str) -> str:
    cleaned = QUIZ_PATTERNS.sub("", user_input)
    cleaned = re.sub(r"\b(give me a|on|about|for|please)\b", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip() or user_input

def route(user_input: str) -> OrchestratorResponse:
    intent = _classify(user_input)
    if intent == "quiz":
        topic = _extract_topic(user_input)
        questions = generate_quiz(topic, num_questions=5)
        payload = {"questions": [q.model_dump() for q in questions]}
    else:
        tutor_response = answer_question(user_input)
        payload = tutor_response.model_dump()
    return OrchestratorResponse(intent=intent, payload=payload)
