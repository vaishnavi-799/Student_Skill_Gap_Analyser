import streamlit as st
from utils.auth import init_session

st.set_page_config(
    page_title="SkillGap AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light theme CSS
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #f0f2f5; color: #1a1f2e; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1a1f2e;
        border-right: none;
    }
    section[data-testid="stSidebar"] * { color: #8892a4 !important; }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] strong { color: #ffffff !important; }
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(45,200,168,0.15) !important;
        color: #2dc8a8 !important;
        border: 1px solid rgba(45,200,168,0.3) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2dc8a8, #3b82f6);
        color: #ffffff;
        font-weight: 600;
        border: none;
        border-radius: 8px;
    }
    .stButton > button:hover { opacity: 0.88; }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetricValue"] { color: #2dc8a8; font-weight: 700; }
    div[data-testid="stMetricLabel"] { color: #6b7280; }
    div[data-testid="stMetricDelta"] { color: #2dc8a8; }

    /* Inputs */
    .stTextInput > div > input,
    .stNumberInput > div > input {
        background-color: #ffffff !important;
        color: #1a1f2e !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div {
        background-color: #ffffff !important;
        color: #1a1f2e !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background: #ffffff; border-radius: 10px; padding: 4px; }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #6b7280;
        border-radius: 8px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #2dc8a8;
        color: #ffffff !important;
        font-weight: 600;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        color: #1a1f2e;
    }
    .streamlit-expanderContent {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-top: none;
        border-radius: 0 0 10px 10px;
    }

    /* Dataframe */
    .stDataFrame { background: #ffffff; border-radius: 10px; }

    /* Text */
    h1, h2, h3 { color: #1a1f2e !important; }
    p, li { color: #374151; }
    hr { border-color: #e5e7eb; }

    /* Info/warning/success boxes */
    .stAlert { border-radius: 10px; }

    /* Progress bar */
    .stProgress > div > div { background: #2dc8a8; }

    /* Cards / containers */
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 12px;
    }
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
col1.metric("Departments",    "5",   "CSE, ECE, MECH, CIVIL, CHEM")
col2.metric("Job Roles",      "30",  "Across all departments")
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