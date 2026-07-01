import streamlit as st
from frontend.api_client import ingest_file

def render_upload():
    st.title("📄 Upload Training Documents")
    uploaded = st.file_uploader("Upload a DOCX file", type=["docx"])
    if uploaded and st.button("Ingest Document"):
        with st.spinner("Ingesting..."):
            result = ingest_file(uploaded.read(), uploaded.name, st.session_state.token)
        st.success(f"Done! {result['chunks_written']} chunks written to collection '{result['collection']}'.")
