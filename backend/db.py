import os
from contextlib import contextmanager
import psycopg2
import psycopg2.extras
from backend.models import EvalResult

DATABASE_URL = os.environ["NEON_DATABASE_URL"]


@contextmanager
def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def save_eval_result(result: EvalResult):
    with get_conn() as conn:
        with conn.cursor() as cur:
            for model, scores in [("claude", result.claude), ("groq", result.groq)]:
                cur.execute(
                    """
                    INSERT INTO eval_scores (question_id, model, accuracy, groundedness, latency_ms)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (result.question_id, model, scores.accuracy, scores.groundedness, scores.latency_ms),
                )


def get_eval_results() -> list[dict]:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM eval_scores ORDER BY run_at DESC")
            return [dict(r) for r in cur.fetchall()]


def save_quiz_result(username: str, question_id: int, is_correct: bool):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO quiz_results (username, question_id, is_correct) VALUES (%s, %s, %s)",
                (username, question_id, is_correct),
            )


def get_quiz_results(username: str) -> list[dict]:
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM quiz_results WHERE username=%s ORDER BY created_at DESC",
                (username,),
            )
            return [dict(r) for r in cur.fetchall()]
