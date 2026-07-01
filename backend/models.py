from pydantic import BaseModel, Field
from typing import List, Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class Citation(BaseModel):
    section: str
    page: int

class TutorRequest(BaseModel):
    question: str

class TutorResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: float = Field(ge=0.0, le=1.0)

class QuizRequest(BaseModel):
    topic: str

class QuizQuestion(BaseModel):
    question: str
    correct_answer: str
    distractors: List[str] = Field(min_length=3, max_length=3)
    source_section: str

class EvalScore(BaseModel):
    accuracy: float = Field(ge=0.0, le=1.0)
    groundedness: float = Field(ge=0.0, le=1.0)
    latency_ms: int

class EvalResult(BaseModel):
    question_id: int
    claude: EvalScore
    groq: EvalScore

class IngestionStatus(BaseModel):
    chunks_written: int
    collection: str
    status: str

class OrchestratorRequest(BaseModel):
    user_input: str

class OrchestratorResponse(BaseModel):
    intent: str  # "question" | "quiz"
    payload: dict
