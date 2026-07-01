import pytest
from unittest.mock import MagicMock
from backend.agents.orchestrator import route
from backend.models import OrchestratorResponse, TutorResponse, Citation, QuizQuestion

def test_routes_question_to_tutor(mocker):
    mock_response = TutorResponse(
        answer="PPE must be worn.", citations=[Citation(section="3.2", page=10)], confidence=0.9
    )
    mocker.patch("backend.agents.orchestrator.answer_question", return_value=mock_response)
    result = route("What is the PPE policy?")
    assert result.intent == "question"
    assert "answer" in result.payload

def test_routes_quiz_request_to_quiz_generator(mocker):
    mock_questions = [
        QuizQuestion(
            question="Q?", correct_answer="A", distractors=["X", "Y", "Z"], source_section="1.1"
        )
    ]
    mocker.patch("backend.agents.orchestrator.generate_quiz", return_value=mock_questions)
    result = route("Give me a quiz on PPE")
    assert result.intent == "quiz"
    assert "questions" in result.payload
