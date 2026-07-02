import streamlit as st

st.set_page_config(page_title="Cortex", page_icon="🟨", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None


def _logout():
    for key in ("token", "role", "chat_history", "quiz", "quiz_submitted"):
        st.session_state.pop(key, None)
    st.session_state.token = None
    st.session_state.role = None


if not st.session_state.token:
    from views.login import render_login
    render_login()
else:
    with st.sidebar:
        st.markdown(
            '<div class="cx-eyebrow">Signed in as '
            f'{st.session_state.role}</div>',
            unsafe_allow_html=True,
        )
        if st.session_state.role == "admin":
            page = st.radio("Navigate", ["Upload documents", "Eval dashboard"])
        else:
            page = None
        st.button("Sign out", on_click=_logout)

    if st.session_state.role == "admin":
        if page == "Upload documents":
            from views.admin_upload import render_upload
            render_upload()
        else:
            from views.eval_dashboard import render_eval
            render_eval()
    else:
        from views.learner import render_learner
        render_learner()
