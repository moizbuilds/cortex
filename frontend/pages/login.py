import streamlit as st
from frontend.api_client import login

def render_login():
    st.title("🧠 Cortex — Corporate Training Platform")
    st.subheader("Sign in")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign in"):
        try:
            data = login(username, password)
            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]
            st.rerun()
        except Exception as e:
            st.error(f"Login failed: {e}")
