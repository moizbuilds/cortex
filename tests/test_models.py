from backend.models import (
    TutorResponse, Citation, QuizQuestion, EvalScore, EvalResult
)

def test_tutor_response_structure():
    r = TutorResponse(
        answer="Safety first.",
        citations=[Citation(section="1.1", page=3)],
        confidence=0.9
    )
    assert r.confidence == 0.9
    assert r.citations[0].page == 3

def test_quiz_question_structure():
    q = QuizQuestion(
        question="What is HSSE?",
        correct_answer="Health, Safety, Security, Environment",
        distractors=["A", "B", "C"],
        source_section="1.2"
    )
    assert len(q.distractors) == 3

def test_eval_result_structure():
    er = EvalResult(
        question_id=1,
        claude=EvalScore(accuracy=0.9, groundedness=0.8, latency_ms=320),
        groq=EvalScore(accuracy=0.7, groundedness=0.6, latency_ms=150)
    )
    assert er.claude.accuracy == 0.9
