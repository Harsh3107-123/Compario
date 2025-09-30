import streamlit as st
from sqlalchemy.exc import IntegrityError

from database import Session
from model import User


st.set_page_config(page_title="Register", page_icon="📝")
st.title("Register")

with st.form("register_form"):
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
    with col2:
        mobile_no = st.text_input("Mobile No (optional)")
        address = st.text_area("Address (optional)")
    submitted = st.form_submit_button("Create Account")

if submitted:
    if not username or not email or not password:
        st.error("Username, Email and Password are required.")
    else:
        session = Session()
        try:
            user = User(
                username=username,
                email=email,
                mobile_no=mobile_no or None,
                address=address or None,
            )
            user.set_password(password)
            session.add(user)
            session.commit()
            st.success("Registration complete. You can now login.")
        except IntegrityError:
            session.rollback()
            st.error("Username or Email already exists.")
        except Exception:
            session.rollback()
            st.error("Registration failed. Please try again.")
        finally:
            session.close()

