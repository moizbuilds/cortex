import streamlit as st
import pandas as pd
from api_client import run_eval, get_eval_results
from theme import inject_theme, brand_header


def render_eval():
    inject_theme()
    brand_header("Model evaluation · Claude vs Groq")

    if st.button("Run evaluation (30 gold Q&A pairs)"):
        with st.spinner("Running both models over the gold set — about 2 minutes…"):
            try:
                run_eval(st.session_state.token)
            except Exception:
                st.error("Evaluation run failed. Check backend logs and API keys.")
                return
        st.success("Evaluation complete.")

    try:
        data = get_eval_results(st.session_state.token)
    except Exception:
        st.error("Couldn't load results. Check that the backend and database are running.")
        return
    results = data.get("results", [])
    if not results:
        st.info("No results yet. Run an evaluation to score both models against the gold set.")
        return

    df = pd.DataFrame(results)
    claude_rows = df[df["model"] == "claude"]
    groq_rows = df[df["model"] == "groq"]

    st.subheader("Aggregate scores")
    agg = pd.DataFrame({
        "Model": ["Claude", "Groq"],
        "Avg Accuracy": [claude_rows["accuracy"].mean(), groq_rows["accuracy"].mean()],
        "Avg Groundedness": [claude_rows["groundedness"].mean(), groq_rows["groundedness"].mean()],
        "Avg Latency (ms)": [claude_rows["latency_ms"].mean(), groq_rows["latency_ms"].mean()],
    })
    st.dataframe(
        agg.style
        .highlight_max(axis=0, subset=["Avg Accuracy", "Avg Groundedness"], color="#EDF5EF")
        .highlight_min(axis=0, subset=["Avg Latency (ms)"], color="#EDF5EF")
        .format({"Avg Accuracy": "{:.3f}", "Avg Groundedness": "{:.3f}", "Avg Latency (ms)": "{:.0f}"}),
        use_container_width=True, hide_index=True,
    )
    st.bar_chart(
        agg.set_index("Model")[["Avg Accuracy", "Avg Groundedness"]],
        color=["#005EB8", "#FFC400"],
    )
    st.bar_chart(agg.set_index("Model")[["Avg Latency (ms)"]], color=["#1A2332"])

    st.subheader("Per-question breakdown")
    for qid in sorted(df["question_id"].unique()):
        q_df = df[df["question_id"] == qid]
        c_rows = q_df[q_df["model"] == "claude"]
        g_rows = q_df[q_df["model"] == "groq"]
        if c_rows.empty or g_rows.empty:
            continue
        claude, groq = c_rows.iloc[0], g_rows.iloc[0]
        winner = "Claude" if claude["accuracy"] >= groq["accuracy"] else "Groq"
        with st.expander(f"Question {qid} — winner: {winner}"):
            st.markdown(f'<span class="cx-winner">{winner}</span>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            for col, name, row in ((c1, "Claude", claude), (c2, "Groq", groq)):
                with col:
                    st.markdown(f"**{name}**")
                    st.metric("Accuracy", f"{row['accuracy']:.3f}")
                    st.metric("Groundedness", f"{row['groundedness']:.3f}")
                    st.metric("Latency", f"{row['latency_ms']} ms")
