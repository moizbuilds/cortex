import pytest
import os
from unittest.mock import patch, MagicMock
from backend.db import save_eval_result, get_eval_results
from backend.models import EvalResult, EvalScore


@pytest.fixture
def mock_conn(mocker):
    mock_cursor = MagicMock()
    mock_cursor.__enter__ = lambda s: s
    mock_cursor.__exit__ = MagicMock(return_value=False)
    mock_connection = MagicMock()
    mock_connection.__enter__ = lambda s: s
    mock_connection.__exit__ = MagicMock(return_value=False)
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch("backend.db.get_conn", return_value=mock_connection)
    return mock_cursor


def test_save_eval_result_calls_db(mock_conn):
    result = EvalResult(
        question_id=1,
        claude=EvalScore(accuracy=0.9, groundedness=0.8, latency_ms=300),
        groq=EvalScore(accuracy=0.7, groundedness=0.6, latency_ms=120),
    )
    save_eval_result(result)
    assert mock_conn.execute.call_count == 2
