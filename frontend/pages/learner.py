import streamlit as st
from frontend.api_client import chat, get_quiz

def render_learner():
    st.title("🧠 Cortex — Learning Assistant")
    tab1, tab2 = st.tabs(["Ask a Question", "Take a Quiz"])

    with tab1:
        question = st.text_input("Ask anything about your training materials")
        if st.button("Ask") and question:
            with st.spinner("Thinking..."):
                result = chat(question, st.session_state.token)
            if result["intent"] == "question":
                payload = result["payload"]
                st.markdown(f"**Answer:** {payload['answer']}")
                if payload.get("citations"):
                    st.markdown("**Sources:**")
                    for c in payload["citations"]:
                        st.markdown(f"- Section {c['section']}, Page {c['page']}")
                st.caption(f"Confidence: {payload.get('confidence', 0):.0%}")

    with tab2:
        topic = st.text_input("Enter a topic for your quiz (e.g. PPE, emergency procedures)")
        if st.button("Generate Quiz") and topic:
            with st.spinner("Generating quiz..."):
                data = get_quiz(topic, st.session_state.token)
            questions = data.get("questions", [])
            st.session_state["quiz"] = questions
            st.session_state["answers"] = {}

        if st.session_state.get("quiz"):
            quiz = st.session_state["quiz"]
            for i, q in enumerate(quiz):
                options = [q["correct_answer"]] + q["distractors"]
                options = sorted(options)
                choice = st.radio(f"**Q{i+1}: {q['question']}**", options, key=f"q{i}")
                st.session_state["answers"][i] = (choice, q["correct_answer"])

            if st.button("Submit Quiz"):
                score = sum(1 for c, a in st.session_state["answers"].values() if c == a)
                st.success(f"Score: {score}/{len(quiz)}")
                for i, (choice, correct) in st.session_state["answers"].items():
                    if choice == correct:
                        st.markdown(f"✅ Q{i+1}: Correct")
                    else:
                        st.markdown(f"❌ Q{i+1}: Correct answer was **{correct}**")
