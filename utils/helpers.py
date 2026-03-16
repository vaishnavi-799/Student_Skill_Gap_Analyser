import streamlit as st
from config.supabase_client import get_supabase

DEPT_ROLES = {
    "CSE":   ["Software Developer","Data Scientist","Web Developer","DevOps Engineer",
               "ML Engineer","Cybersecurity Analyst","Product Manager"],
    "ECE":   ["Embedded Systems Engineer","VLSI Design Engineer","IoT Developer",
               "Signal Processing Engineer","Telecom Engineer","Hardware Design Engineer"],
    "MECH":  ["Mechanical Design Engineer","Manufacturing Engineer","Automobile Engineer",
               "Thermal Engineer","Robotics Engineer","Quality Control Engineer"],
    "CIVIL": ["Structural Engineer","Site Engineer","Urban Planner",
               "Environmental Engineer","Construction Manager","Geotechnical Engineer"],
    "CHEM":  ["Process Engineer","Quality Assurance Engineer","R&D Chemist",
               "Petrochemical Engineer","Pharmaceutical Engineer"],
}

COLLEGE_TIERS = {
    1: {"label": "Tier 1 — IIT / IISc",           "weight": 1.00},
    2: {"label": "Tier 2 — NIT / BITS / IIIT",    "weight": 0.85},
    3: {"label": "Tier 3 — State Govt University", "weight": 0.70},
    4: {"label": "Tier 4 — Private Tier-A",        "weight": 0.60},
    5: {"label": "Tier 5 — Private Tier-B/C",      "weight": 0.45},
}

def get_roles_for_dept(dept: str) -> list:
    return DEPT_ROLES.get(dept, [])

def get_role_id_by_name(role_name: str) -> str:
    supabase = get_supabase()
    res = supabase.table("job_roles").select("role_id").eq("role_name", role_name).execute()
    return res.data[0]["role_id"] if res.data else None

def get_role_skills(role_id: str) -> dict:
    supabase = get_supabase()
    res = supabase.table("job_roles").select("*").eq("role_id", role_id).execute()
    if not res.data:
        return {}
    role = res.data[0]
    skill_ids  = role["required_skill_ids"].split(",")
    benchmarks = list(map(int, role["benchmark_scores"].split(",")))
    skills_res = supabase.table("skills").select("skill_id,skill_name").in_("skill_id", skill_ids).execute()
    name_map   = {s["skill_id"]: s["skill_name"] for s in skills_res.data}
    return {name_map.get(sk, sk): {"skill_id": sk, "benchmark": b}
            for sk, b in zip(skill_ids, benchmarks)}

def get_topics_for_skill(skill_id: str) -> list:
    supabase = get_supabase()
    res = supabase.table("skill_topics").select("*").eq("skill_id", skill_id).execute()
    return res.data or []

def save_student_profile(profile: dict) -> bool:
    try:
        supabase = get_supabase()
        supabase.table("students").upsert(profile).execute()
        return True
    except Exception as e:
        st.error(f"Error saving profile: {e}")
        return False

def save_skill_scores(student_id: str, scores: list) -> bool:
    try:
        supabase = get_supabase()
        for score in scores:
            score["student_id"] = student_id
        supabase.table("student_skill_scores").upsert(scores).execute()
        return True
    except Exception as e:
        st.error(f"Error saving scores: {e}")
        return False

def format_pct(val: float) -> str:
    return f"{val:.1f}%"

def priority_color(priority: str) -> str:
    return {"high": "#ff4560", "medium": "#ffc837", "low": "#00e5c3"}.get(priority, "#5a7090")
