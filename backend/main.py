from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from backend.models import (
    LoginRequest, TokenResponse, TutorRequest, TutorResponse,
    QuizRequest, OrchestratorRequest, OrchestratorResponse, IngestionStatus
)
from backend.auth import authenticate_user, create_token
from backend.deps import get_current_user, require_admin
from backend.agents.orchestrator import route
from backend.ingestion import ingest_docx
from backend.db import get_eval_results
from pathlib import Path
import json

app = FastAPI(title="Cortex API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = authenticate_user(body.username, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Bad credentials")
    return TokenResponse(access_token=create_token(user["username"], user["role"]), role=user["role"])


@app.post("/chat", response_model=OrchestratorResponse)
def chat(body: OrchestratorRequest, user: dict = Depends(get_current_user)):
    return route(body.user_input)


@app.post("/quiz")
def quiz(body: QuizRequest, user: dict = Depends(get_current_user)):
    from backend.agents.quiz_generator import generate_quiz
    questions = generate_quiz(body.topic)
    return {"questions": [q.model_dump() for q in questions]}


@app.post("/ingest", response_model=IngestionStatus)
async def ingest(file: UploadFile = File(...), user: dict = Depends(require_admin)):
    contents = await file.read()
    return ingest_docx(contents)


@app.post("/eval/run")
def eval_run(user: dict = Depends(require_admin)):
    gold_qa_path = Path(__file__).parent.parent / "data" / "gold_qa.json"
    with open(gold_qa_path) as f:
        gold_qa = json.load(f)
    from backend.agents.evaluator import run_evaluation
    results = run_evaluation(gold_qa)
    return {"results": [r.model_dump() for r in results]}


@app.get("/eval/results")
def eval_results(user: dict = Depends(require_admin)):
    return {"results": get_eval_results()}
