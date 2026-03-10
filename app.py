import streamlit as st
from utils.auth import init_session

st.set_page_config(
    page_title="SkillGap AI — Engineering",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS
st.markdown("""
<style>
    .stApp { background-color: #070b14; color: #dce8f5; }
    section[data-testid="stSidebar"] { background-color: #0e1420; border-right: 1px solid #1e2d45; }
    .stButton > button { background: linear-gradient(135deg,#00e5c3,#4d9fff); color: #070b14; font-weight: 700; border: none; border-radius: 8px; }
    .stButton > button:hover { opacity: 0.85; }
    div[data-testid="stMetric"] { background: #0e1420; border: 1px solid #1e2d45; border-radius: 10px; padding: 12px; }
    div[data-testid="stMetricValue"] { color: #00e5c3; font-weight: 700; }
    .stTextInput > div > input, .stSelectbox > div, .stNumberInput > div > input { background-color: #0e1420 !important; color: #dce8f5 !important; border: 1px solid #1e2d45 !important; border-radius: 8px !important; }
    .stSlider > div > div { background: #1e2d45; }
    .stDataFrame { background: #0e1420; }
    h1, h2, h3 { color: #dce8f5 !important; }
    .stMarkdown p { color: #dce8f5; }
    hr { border-color: #1e2d45; }
    .stTabs [data-baseweb="tab"] { background: #0e1420; color: #5a7090; border-radius: 8px 8px 0 0; }
    .stTabs [aria-selected="true"] { background: #00e5c3; color: #070b14; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

init_session()

st.sidebar.markdown("## 🎓 SkillGap AI")
st.sidebar.markdown("**Engineering Edition**")
st.sidebar.markdown("---")

if st.session_state.logged_in:
    st.sidebar.markdown(f"👤 **{st.session_state.get('student_name','Student')}**")
    st.sidebar.markdown(f"🏛️ {st.session_state.get('department','—')}")
    st.sidebar.markdown("---")
    if st.sidebar.button("⏻ Logout"):
        from utils.auth import logout
        logout()

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:10px;color:#5a7090'>ML Engine Active<br>Topic-Weighted · Domain-Aware</div>",
    unsafe_allow_html=True
)

# Home content
st.title("🎓 Student Skill Gap Analyzer & Upskill Tracker")
st.markdown("##### *Engineering Edition — CSE · ECE · MECH · CIVIL · CHEM*")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Departments", "5", "CSE, ECE, MECH, CIVIL, CHEM")
col2.metric("Job Roles", "30", "Across all departments")
col3.metric("Skills Tracked", "80+", "With topic-wise scoring")

st.markdown("---")
st.markdown("""
### How It Works
1. **📋 Profile** — Enter your details, department, target role and college tier
2. **🛠️ Skills** — Tick topics you know — score is auto-calculated
3. **📋 Credentials** — Add projects, certs, internships with domain tags
4. **📊 Gap Analysis** — See your readiness score, radar chart and skill gaps
5. **🚀 Roadmap** — Get a priority-ranked upskilling plan with courses
6. **✅ Tracker** — Log daily learning tasks and track your streak
7. **📈 Progress** — Re-rate skills after upskilling and see improvement

👈 **Use the sidebar to navigate between pages.**
""")

if not st.session_state.logged_in:
    st.info("👈 Go to **Login** page from the sidebar to get started.")
