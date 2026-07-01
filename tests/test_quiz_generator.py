import pytest
from unittest.mock import MagicMock
from backend.agents.quiz_generator import generate_quiz
from backend.models import QuizQuestion

def test_generate_quiz_returns_questions(mocker):
    mocker.patch(
        "backend.agents.quiz_generator.search",
        return_value=[{"text": "PPE must be worn at all times on site.", "section": "3.2", "page": 10}],
    )
    single_q = '{"question": "When must PPE be worn?", "correct_answer": "At all times on site", "distractors": ["Never", "Only in emergencies", "At management discretion"], "source_section": "3.2"}'
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text=f"[{single_q}]")]
    mocker.patch("backend.agents.quiz_generator.anthropic_client.messages.create", return_value=mock_message)

    questions = generate_quiz("PPE", num_questions=1)
    assert len(questions) == 1
    assert isinstance(questions[0], QuizQuestion)
    assert len(questions[0].distractors) == 3
