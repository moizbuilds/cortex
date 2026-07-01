import streamlit as st

st.set_page_config(page_title="Cortex", page_icon="🧠", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.token:
    from frontend.pages.login import render_login
    render_login()
elif st.session_state.role == "admin":
    page = st.sidebar.selectbox("Navigate", ["Upload Documents", "Eval Dashboard"])
    if page == "Upload Documents":
        from frontend.pages.admin_upload import render_upload
        render_upload()
    else:
        from frontend.pages.eval_dashboard import render_eval
        render_eval()
else:
    from frontend.pages.learner import render_learner
    render_learner()
