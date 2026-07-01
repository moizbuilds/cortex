import pytest
from unittest.mock import MagicMock, patch
from backend.agents.evaluator import score_answer

def test_score_answer_high_similarity():
    gold = "PPE must be worn at all times on site."
    response = "Personal Protective Equipment must be worn at all times on site."
    chunks = ["PPE must be worn at all times on site."]
    accuracy, groundedness = score_answer(gold, response, chunks)
    assert accuracy > 0.5
    assert groundedness > 0.5

def test_score_answer_low_similarity():
    gold = "PPE must be worn at all times on site."
    response = "The sky is blue and the grass is green."
    chunks = ["PPE must be worn at all times on site."]
    accuracy, groundedness = score_answer(gold, response, chunks)
    assert accuracy < 0.5
