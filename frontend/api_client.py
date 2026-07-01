import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def login(username: str, password: str) -> dict:
    r = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
    r.raise_for_status()
    return r.json()

def chat(user_input: str, token: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/chat",
        json={"user_input": user_input},
        headers={"Authorization": f"Bearer {token}"},
    )
    r.raise_for_status()
    return r.json()

def get_quiz(topic: str, token: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/quiz",
        json={"topic": topic},
        headers={"Authorization": f"Bearer {token}"},
    )
    r.raise_for_status()
    return r.json()

def ingest_file(file_bytes: bytes, filename: str, token: str) -> dict:
    r = requests.post(
        f"{BASE_URL}/ingest",
        files={"file": (filename, file_bytes, "application/octet-stream")},
        headers={"Authorization": f"Bearer {token}"},
    )
    r.raise_for_status()
    return r.json()

def run_eval(token: str) -> dict:
    r = requests.post(f"{BASE_URL}/eval/run", headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.json()

def get_eval_results(token: str) -> dict:
    r = requests.get(f"{BASE_URL}/eval/results", headers={"Authorization": f"Bearer {token}"})
    r.raise_for_status()
    return r.json()
