import pytest
from backend.auth import create_token, verify_token


def test_create_and_verify_token():
    token = create_token("alice", "learner")
    payload = verify_token(token)
    assert payload["sub"] == "alice"
    assert payload["role"] == "learner"


def test_verify_bad_token_raises():
    with pytest.raises(Exception):
        verify_token("not.a.real.token")
