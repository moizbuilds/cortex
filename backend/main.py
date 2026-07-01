from fastapi import FastAPI, Depends, HTTPException
from backend.models import LoginRequest, TokenResponse
from backend.auth import authenticate_user, create_token

app = FastAPI(title="Cortex API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = authenticate_user(body.username, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Bad credentials")
    token = create_token(user["username"], user["role"])
    return TokenResponse(access_token=token, role=user["role"])
