import streamlit as st
from utils.auth import init_session, login, signup

st.set_page_config(page_title="Login — SkillGap AI", page_icon="🔐", layout="centered")
init_session()

if st.session_state.logged_in:
    st.success(f"✅ Already logged in as {st.session_state.student_name}")
    st.info("👈 Navigate using the sidebar.")
    st.stop()

st.title("🔐 Login / Sign Up")
st.markdown("---")

tab1, tab2 = st.tabs(["Sign In", "Sign Up"])

with tab1:
    st.subheader("Sign In")
    email    = st.text_input("Email",    key="li_email")
    password = st.text_input("Password", type="password", key="li_pass")
    if st.button("Sign In", key="li_btn"):
        if not email or not password:
            st.error("Please enter email and password.")
        elif login(email, password):
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")

with tab2:
    st.subheader("Create Account")
    name     = st.text_input("Full Name",        key="su_name")
    email_s  = st.text_input("Email",            key="su_email")
    password_s = st.text_input("Password (min 6 characters)", type="password", key="su_pass")
    if st.button("Create Account", key="su_btn"):
        if not name or not email_s or len(password_s) < 6:
            st.error("Please fill all fields. Password must be at least 6 characters.")
        elif signup(email_s, password_s, name):
            st.success("✅ Account created! Redirecting...")
            st.rerun()
        else:
            st.error("❌ Signup failed. Email may already be registered.")
