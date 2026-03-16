import streamlit as st
from config.supabase_client import get_supabase

def init_session():
    defaults = {
        "logged_in": False,
        "student_id": None,
        "student_name": None,
        "department": None,
        "target_role_id": None,
        "target_role_name": None,
        "skill_scores": {},
        "gap_result": {},
        "readiness": 0,
        "cosine": 0,
        "placement": 0,
        "roadmap": [],
        "score_breakdown": {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def login(email: str, password: str) -> bool:
    try:
        supabase = get_supabase()
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if res.user:
            st.session_state.logged_in = True
            st.session_state.student_id = res.user.id
            return True
    except Exception:
        pass
    return False

def signup(email: str, password: str, name: str) -> bool:
    try:
        supabase = get_supabase()
        res = supabase.auth.sign_up({"email": email, "password": password})
        if res.user:
            st.session_state.logged_in = True
            st.session_state.student_id = res.user.id
            st.session_state.student_name = name
            return True
    except Exception:
        pass
    return False

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def require_login():
    init_session()
    if not st.session_state.logged_in:
        st.warning(" Please login first from the Home page.")
        st.stop()
