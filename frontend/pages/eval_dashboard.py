import streamlit as st
import pandas as pd
from frontend.api_client import run_eval, get_eval_results

def render_eval():
    st.title("📊 Model Evaluation Dashboard — Claude vs Groq")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ Run Evaluation (30 Q&A pairs)"):
            with st.spinner("Running evaluation — this takes ~2 minutes..."):
                run_eval(st.session_state.token)
            st.success("Evaluation complete.")

    data = get_eval_results(st.session_state.token)
    results = data.get("results", [])
    if not results:
        st.info("No evaluation results yet. Run an evaluation above.")
        return

    df = pd.DataFrame(results)

    claude_rows = df[df["model"] == "claude"]
    groq_rows = df[df["model"] == "groq"]

    st.subheader("Aggregate Scores")
    agg = pd.DataFrame({
        "Model": ["Claude", "Groq"],
        "Avg Accuracy": [claude_rows["accuracy"].mean(), groq_rows["accuracy"].mean()],
        "Avg Groundedness": [claude_rows["groundedness"].mean(), groq_rows["groundedness"].mean()],
        "Avg Latency (ms)": [claude_rows["latency_ms"].mean(), groq_rows["latency_ms"].mean()],
    })
    st.dataframe(agg.style.highlight_max(axis=0, subset=["Avg Accuracy", "Avg Groundedness"]), use_container_width=True)
    st.bar_chart(agg.set_index("Model")[["Avg Accuracy", "Avg Groundedness"]])

    st.subheader("Per-Question Breakdown")
    for qid in sorted(df["question_id"].unique()):
        q_df = df[df["question_id"] == qid]
        claude = q_df[q_df["model"] == "claude"].iloc[0] if not q_df[q_df["model"] == "claude"].empty else None
        groq = q_df[q_df["model"] == "groq"].iloc[0] if not q_df[q_df["model"] == "groq"].empty else None
        if claude is not None and groq is not None:
            winner = "Claude" if claude["accuracy"] >= groq["accuracy"] else "Groq"
            with st.expander(f"Q{qid} — Winner: {winner}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Claude**")
                    st.metric("Accuracy", f"{claude['accuracy']:.2f}")
                    st.metric("Groundedness", f"{claude['groundedness']:.2f}")
                    st.metric("Latency", f"{claude['latency_ms']}ms")
                with c2:
                    st.markdown("**Groq**")
                    st.metric("Accuracy", f"{groq['accuracy']:.2f}")
                    st.metric("Groundedness", f"{groq['groundedness']:.2f}")
                    st.metric("Latency", f"{groq['latency_ms']}ms")
