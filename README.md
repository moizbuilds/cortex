# Cortex — AI Corporate Training Platform

**RAG pipeline · Multi-agent orchestration · Evaluation harness · Structured output**

Built as part of [30 Apps in 30 Days](https://github.com/moizbuilds).

## What it does

Cortex lets organisations upload training documents and immediately query them with an AI tutor grounded in their own content. Learners ask questions and take AI-generated quizzes. Admins see a live evaluation dashboard comparing Claude vs Groq on accuracy, groundedness, and latency across 30 gold Q&A pairs.

## Architecture

```
[Streamlit UI] → [FastAPI on Cloud Run]
                        ├── Orchestrator Agent
                        │     ├── Tutor Agent → [Qdrant vector store]
                        │     ├── Quiz Generator Agent → [Qdrant]
                        │     └── Evaluator Agent → [Claude] [Groq]
                        └── Ingestion Pipeline (DOCX → chunks → embeddings → Qdrant)
[Neon PostgreSQL] ← quiz results, eval scores
```

## Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Vector DB | Qdrant |
| Relational DB | Neon PostgreSQL |
| LLMs | Claude (Haiku) + Groq (Llama 3 8B) |
| Embeddings | sentence-transformers all-MiniLM-L6-v2 |
| Auth | JWT, role-based (admin / learner) |
| Deploy | Google Cloud Run |

## Running locally

```bash
cp .env.example .env  # fill in your keys
docker compose up
```

## Demo credentials

- Admin: `admin` / `admin123`
- Learner: `learner` / `learn123`
