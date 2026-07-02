import streamlit as st
from api_client import ingest_file
from theme import inject_theme, brand_header


def render_upload():
    inject_theme()
    brand_header("Document ingestion · admin")
    st.markdown(
        "Upload a training manual (DOCX). Cortex splits it into sections, "
        "indexes them for search, and the tutor starts citing it immediately."
    )
    uploaded = st.file_uploader("Training document", type=["docx"])
    if uploaded and st.button("Ingest document"):
        with st.spinner(f"Ingesting {uploaded.name}…"):
            try:
                result = ingest_file(uploaded.read(), uploaded.name, st.session_state.token)
            except Exception:
                st.error("Ingestion failed. Check that the backend and vector store are running.")
                return
        st.success(
            f"Ingested {uploaded.name}: {result['chunks_written']} sections "
            f"indexed into '{result['collection']}'."
        )
