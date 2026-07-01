import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.auth import create_token

client = TestClient(app)

def admin_headers():
    return {"Authorization": f"Bearer {create_token('admin', 'admin')}"}

def learner_headers():
    return {"Authorization": f"Bearer {create_token('learner', 'learner')}"}

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_login_success():
    r = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_fail():
    r = client.post("/auth/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401

def test_chat_requires_auth():
    r = client.post("/chat", json={"user_input": "What is HSSE?"})
    assert r.status_code == 403

def test_ingest_requires_admin():
    r = client.post(
        "/ingest",
        files={"file": ("test.docx", b"fake", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        headers=learner_headers(),
    )
    assert r.status_code == 403
