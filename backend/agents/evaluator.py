import os
import time
import json
import anthropic
from groq import Groq
from sentence_transformers import SentenceTransformer, util
from backend.qdrant_client import search
from backend.models import EvalResult, EvalScore
from backend.db import save_eval_result

anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
_embedder = None

def _get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

CLAUDE_MODEL = "claude-haiku-4-5-20251001"
GROQ_MODEL = "llama3-8b-8192"

RAG_SYSTEM_PROMPT = "Answer the question using only the provided context. Be concise."

def _rag_prompt(question: str, chunks: list[dict]) -> str:
    context = "\n".join(c["text"] for c in chunks)
    return f"Context:\n{context}\n\nQuestion: {question}"

def score_answer(gold: str, response: str, chunks: list[str]) -> tuple[float, float]:
    embedder = _get_embedder()
    gold_vec = embedder.encode(gold, convert_to_tensor=True)
    resp_vec = embedder.encode(response, convert_to_tensor=True)
    accuracy = float(util.cos_sim(gold_vec, resp_vec)[0][0])
    accuracy = max(0.0, min(1.0, accuracy))

    chunk_vecs = _get_embedder().encode(chunks, convert_to_tensor=True)
    if len(chunk_vecs.shape) == 1:
        chunk_vecs = chunk_vecs.unsqueeze(0)
    groundedness_scores = util.cos_sim(resp_vec, chunk_vecs)[0]
    groundedness = float(groundedness_scores.max())
    groundedness = max(0.0, min(1.0, groundedness))

    return accuracy, groundedness

def _query_claude(question: str, chunks: list[dict]) -> tuple[str, int]:
    t0 = time.time()
    msg = anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        system=RAG_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _rag_prompt(question, chunks)}],
    )
    latency = int((time.time() - t0) * 1000)
    return msg.content[0].text, latency

def _query_groq(question: str, chunks: list[dict]) -> tuple[str, int]:
    t0 = time.time()
    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {"role": "user", "content": _rag_prompt(question, chunks)},
        ],
        max_tokens=512,
    )
    latency = int((time.time() - t0) * 1000)
    return completion.choices[0].message.content, latency

def run_evaluation(gold_qa: list[dict]) -> list[EvalResult]:
    results = []
    for item in gold_qa:
        chunks = search(item["question"], top_k=5)
        chunk_texts = [c["text"] for c in chunks]

        claude_answer, claude_latency = _query_claude(item["question"], chunks)
        groq_answer, groq_latency = _query_groq(item["question"], chunks)

        claude_acc, claude_ground = score_answer(item["answer"], claude_answer, chunk_texts)
        groq_acc, groq_ground = score_answer(item["answer"], groq_answer, chunk_texts)

        result = EvalResult(
            question_id=item["id"],
            claude=EvalScore(accuracy=claude_acc, groundedness=claude_ground, latency_ms=claude_latency),
            groq=EvalScore(accuracy=groq_acc, groundedness=groq_ground, latency_ms=groq_latency),
        )
        save_eval_result(result)
        results.append(result)
    return results
