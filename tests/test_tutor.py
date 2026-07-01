import pytest
from unittest.mock import patch, MagicMock
from backend.agents.tutor import answer_question
from backend.models import TutorResponse

def test_answer_question_returns_tutor_response(mocker):
    mocker.patch(
        "backend.agents.tutor.search",
        return_value=[
            {"text": "HSSE means Health, Safety, Security, Environment.", "section": "1.1", "page": 1}
        ],
    )
    mock_message = MagicMock()
    mock_message.content = [MagicMock(text='{"answer": "HSSE stands for Health, Safety, Security, Environment.", "citations": [{"section": "1.1", "page": 1}], "confidence": 0.95}')]
    mocker.patch("backend.agents.tutor.anthropic_client.messages.create", return_value=mock_message)

    result = answer_question("What does HSSE stand for?")
    assert isinstance(result, TutorResponse)
    assert "HSSE" in result.answer
    assert result.confidence == 0.95
