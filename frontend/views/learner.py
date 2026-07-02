import streamlit as st
from api_client import chat, get_quiz
from theme import inject_theme, brand_header, citation_tags


def _render_answer(payload: dict):
    st.markdown(payload["answer"])
    if payload.get("citations"):
        st.markdown(citation_tags(payload["citations"]), unsafe_allow_html=True)
    st.markdown(
        f'<div class="cx-confidence">Confidence {payload.get("confidence", 0):.0%}</div>',
        unsafe_allow_html=True,
    )


def _render_chat_tab():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for entry in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(entry["question"])
        with st.chat_message("assistant"):
            _render_answer(entry["payload"])

    # st.chat_input is not allowed inside st.tabs — use a form instead
    with st.form("ask", clear_on_submit=True):
        question = st.text_input(
            "Your question", placeholder="Ask about your training materials…"
        )
        asked = st.form_submit_button("Ask")
    if asked and question:
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Checking the manual…"):
                try:
                    result = chat(question, st.session_state.token)
                except Exception:
                    st.error("Couldn't reach the tutor. Try again in a moment.")
                    return
            if result["intent"] == "question":
                _render_answer(result["payload"])
                st.session_state.chat_history.append(
                    {"question": question, "payload": result["payload"]}
                )
            else:
                st.info("That looks like a quiz request — use the Take a Quiz tab.")


def _render_quiz_tab():
    with st.form("quiz_request"):
        topic = st.text_input(
            "Quiz topic", placeholder="e.g. PPE, permits, emergency procedures…"
        )
        requested = st.form_submit_button("Generate quiz")
    if requested and topic:
        with st.spinner("Writing questions from the manual…"):
            try:
                data = get_quiz(topic, st.session_state.token)
            except Exception:
                st.error("Couldn't generate a quiz. Try again in a moment.")
                return
        questions = data.get("questions", [])
        if not questions:
            st.info("No questions came back for that topic — try a broader one.")
            return
        st.session_state.quiz = questions
        st.session_state.quiz_submitted = False

    quiz = st.session_state.get("quiz")
    if not quiz:
        return

    with st.form("quiz_answers"):
        answers = {}
        for i, q in enumerate(quiz):
            options = sorted([q["correct_answer"]] + q["distractors"])
            answers[i] = st.radio(
                f"**Q{i + 1}: {q['question']}**", options, index=None, key=f"q{i}"
            )
        submitted = st.form_submit_button("Submit answers")

    if submitted:
        unanswered = [i + 1 for i, a in answers.items() if a is None]
        if unanswered:
            st.warning(f"Answer question{'s' if len(unanswered) > 1 else ''} "
                       f"{', '.join(map(str, unanswered))} before submitting.")
            return
        score = sum(1 for i, q in enumerate(quiz) if answers[i] == q["correct_answer"])
        st.markdown(f"### Score: {score}/{len(quiz)}")
        for i, q in enumerate(quiz):
            if answers[i] == q["correct_answer"]:
                st.markdown(f'<div class="cx-correct">Q{i + 1} — Correct</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="cx-wrong">Q{i + 1} — Correct answer: '
                    f'<strong>{q["correct_answer"]}</strong></div>',
                    unsafe_allow_html=True,
                )


def render_learner():
    inject_theme()
    brand_header("Learning assistant · answers cited to the manual")
    tab1, tab2 = st.tabs(["Ask a question", "Take a quiz"])
    with tab1:
        _render_chat_tab()
    with tab2:
        _render_quiz_tab()
