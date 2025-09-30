import streamlit as st
from database import Session
from model import User


st.set_page_config(page_title="Login", page_icon="🔐")
st.title("Login")

with st.form("login_form"):
    username_or_email = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

if submitted:
    if not username_or_email or not password:
        st.error("Please fill in all fields.")
    else:
        session = Session()
        try:
            user = (
                session.query(User)
                .filter((User.username == username_or_email) | (User.email == username_or_email))
                .first()
            )
            if user and user.check_password(password):
                st.success(f"Welcome, {user.username}!")
                st.info("Use the sidebar to go to Dashboard.")
            else:
                st.error("Invalid credentials.")
        finally:
            session.close()

