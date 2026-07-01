# Cortex — Design Spec
**Date:** 2026-07-01  
**Project:** 30 apps in 30 days — App 9  
**Status:** Approved, ready for implementation

---

## 1. What It Is

Cortex is an AI-powered corporate training platform. An organisation uploads their documents. Cortex ingests them, chunks and embeds them into a vector store, and grounds an AI tutor in that corpus. Learners ask questions, take AI-generated quizzes, and get graded. An admin dashboard shows learner outcomes and a side-by-side model evaluation comparing Claude vs Groq on accuracy, groundedness, and latency.

**Portfolio purpose:** Proves RAG pipeline design, multi-agent orchestration, model evaluation harness, structured output, and enterprise/government use case — all in one app. Directly targets Scale AI Global Public Sector AI Product Leader and Solutions Architect roles.

---

## 2. Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python) |
| Backend | FastAPI on Cloud Run |
| Vector DB | Qdrant (Docker container) |
| Relational DB | PostgreSQL on Neon |
| LLMs | Claude API (primary) + Groq (comparison) |
| Auth | JWT, role-based (admin / learner) |
| Deploy | Cloud Run (backend, Qdrant, Streamlit) |
| Demo corpus | Soltech SC-HSSE-3.0 HSSE Policy Statement & Manual |

Everything is Python. Everything is containerised.

---

## 3. Architecture

```
[Streamlit UI]
      |
      | JWT-authenticated HTTP
      v
[FastAPI — Cloud Run]
      |
      |--- Orchestrator Agent
      |         |--- Tutor Agent ---------> [Qdrant vector store]
      |         |--- Quiz Generator Agent -> [Qdrant vector store]
      |         |--- Evaluator Agent ------> [Claude API] [Groq API]
      |
      |--- Ingestion Pipeline (admin only)
      |         |--- Parse DOCX
      |         |--- Chunk + Embed
      |         |--- Write to Qdrant
      |
[PostgreSQL on Neon]
      - users, roles, sessions
      - quiz results
      - eval scores (per question, per model, per run)
```

---

## 4. Agents

### Orchestrator
Receives learner input, classifies intent (question vs quiz request), routes to the correct agent. Returns structured JSON response to Streamlit.

### Tutor Agent
- Receives a question from the learner
- Retrieves top-k relevant chunks from Qdrant via semantic search
- Passes chunks + question to Claude with a strict system prompt grounding it in the document
- Returns answer + citations (which section the answer came from)
- Structured JSON output: `{ answer, citations: [{ section, page }], confidence }`

### Quiz Generator Agent
- Receives a topic or document section
- Retrieves relevant chunks from Qdrant
- Uses Claude to generate questions with one correct answer and three plausible wrong answers (Haiku-style distractor generation)
- Structured JSON output: `{ question, correct_answer, distractors: [x3], source_section }`

### Evaluator Agent
- Takes each gold Q&A pair
- Runs it through Claude AND Groq independently
- Scores each response on:
  - **Accuracy** — semantic similarity to gold answer (0–1)
  - **Groundedness** — does the answer cite content that exists in the document (0–1)
  - **Latency** — response time in milliseconds
- Writes scores to Postgres
- Structured JSON output: `{ question_id, claude: { accuracy, groundedness, latency }, groq: { accuracy, groundedness, latency } }`

---

## 5. Ingestion Pipeline

1. Admin uploads DOCX via Streamlit
2. FastAPI parses the document (python-docx)
3. Text is chunked (512 tokens, 50-token overlap)
4. Each chunk is embedded (sentence-transformers or Claude embeddings)
5. Embeddings + metadata (section title, page) written to Qdrant
6. Ingestion status returned to admin dashboard

---

## 6. Eval Harness

**Gold Q&A set:** 30 hand-crafted question/answer pairs drawn from the HSSE manual. Ground truth for all scoring.

**Dashboard shows:**
- Claude vs Groq side-by-side on accuracy, groundedness, latency
- Per-question breakdown (where each model wins/loses)
- Aggregate scores over time
- Winner per metric highlighted

**Why this matters:** Almost no portfolio project has a real eval harness with real numbers. This is the differentiator that reads as "this person understands production AI" — which is exactly the Scale AI bar.

---

## 7. Security

- JWT auth on all API endpoints
- Role-based access: admin (upload docs, see eval dashboard) vs learner (chat, take quizzes)
- API keys in environment variables only, never in code
- Document data stays within the platform's own infrastructure
- HTTPS enforced via Cloud Run

---

## 8. Demo Corpus

**File:** `SC-HSSE-3.0 HSSE Policy Statement & Manual[60].docx`  
**Source:** Soltech (real enterprise HSSE document)  
**Gold Q&A set:** 30 pairs to be generated from the document before ingestion

---

## 9. Definition of Done

- [ ] Live deployed URL + public GitHub repo
- [ ] README uses the vocabulary of the JDs: "RAG pipeline," "multi-agent orchestration," "evaluation harness," "structured output with validation"
- [ ] Architecture diagram in README
- [ ] Demo corpus loaded and queryable on first visit
- [ ] Eval dashboard populated with real Claude vs Groq numbers
- [ ] Role-based auth working (admin and learner flows)

---

## 10. How to Talk About It (interviews/resume)

*"Built Cortex, an enterprise AI training platform: RAG-grounded tutor over a real HSSE policy corpus, multi-agent design (orchestrator / tutor / quiz generator / evaluator), an automated evaluation harness scoring Claude vs Groq on accuracy, groundedness, and latency — all Python, deployed on Cloud Run with Qdrant for vector search and Neon Postgres for relational data."*

That single sentence answers RAG, multi-agent, evaluation, model comparison, Python, and enterprise use case at once.
