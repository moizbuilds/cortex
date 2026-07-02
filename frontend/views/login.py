import streamlit as st
from api_client import login
from theme import inject_theme, brand_header


def render_login():
    inject_theme()
    left, _ = st.columns([1, 1])
    with left:
        brand_header("Corporate training · grounded in your documents")
        st.markdown(
            "Ask questions, take quizzes, and get answers cited back to the "
            "exact section of your company's own manuals."
        )
        with st.form("login", border=True):
            username = st.text_input("Username", autocomplete="username")
            password = st.text_input("Password", type="password", autocomplete="current-password")
            submitted = st.form_submit_button("Sign in")
        if submitted:
            if not username or not password:
                st.error("Enter a username and password to sign in.")
                return
            try:
                data = login(username, password)
            except Exception:
                st.error("Sign-in failed. Check your username and password, then try again.")
                return
            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]
            st.rerun()
