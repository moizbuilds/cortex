import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

# (connect, read) seconds. LLM-backed endpoints get long reads; eval runs 30 pairs.
_FAST = (5, 15)
_LLM = (5, 120)
_EVAL = (5, 600)


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def login(username: str, password: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": username, "password": password},
        timeout=_FAST,
    )
    r.raise_for_status()
    return r.json()


def chat(user_input: str, token: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/chat", json={"user_input": user_input},
        headers=_auth(token), timeout=_LLM,
    )
    r.raise_for_status()
    return r.json()


def get_quiz(topic: str, token: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/quiz", json={"topic": topic},
        headers=_auth(token), timeout=_LLM,
    )
    r.raise_for_status()
    return r.json()


def ingest_file(file_bytes: bytes, filename: str, token: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/ingest",
        files={"file": (filename, file_bytes, "application/octet-stream")},
        headers=_auth(token), timeout=_LLM,
    )
    r.raise_for_status()
    return r.json()


def run_eval(token: str) -> dict:
    r = requests.post(f"{BASE_URL}/eval/run", headers=_auth(token), timeout=_EVAL)
    r.raise_for_status()
    return r.json()


def get_eval_results(token: str) -> dict:
    r = requests.get(f"{BASE_URL}/eval/results", headers=_auth(token), timeout=_FAST)
    r.raise_for_status()
    return r.json()
