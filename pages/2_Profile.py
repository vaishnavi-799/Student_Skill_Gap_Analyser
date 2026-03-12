import streamlit as st
from utils.auth import require_login
from utils.helpers import get_roles_for_dept, get_role_id_by_name, save_student_profile
from utils.college_tier import TIER_INFO

require_login()
st.title("📋 Student Profile")
st.markdown("Fill in your academic details and select your target job role.")
st.markdown("---")

DEPTS = ["CSE", "ECE", "MECH", "CIVIL", "CHEM"]

col1, col2 = st.columns(2)
with col1:
    name  = st.text_input("Full Name",    value=st.session_state.get("student_name",""))
    dept  = st.selectbox("Department",    DEPTS)
    year  = st.selectbox("Year of Study", ["1st Year","2nd Year","3rd Year","4th Year"])
    cgpa  = st.number_input("CGPA (out of 10)", min_value=0.0, max_value=10.0, value=7.5, step=0.1)

with col2:
    roll    = st.text_input("Roll Number", placeholder="e.g. 22CS001")
    roles   = get_roles_for_dept(dept)
    role    = st.selectbox("Target Job Role", roles)
    college = st.text_input("College Name", placeholder="e.g. NIT Trichy")
    tier    = st.selectbox("College Tier", options=list(TIER_INFO.keys()),
                           format_func=lambda x: TIER_INFO[x]["label"])

# Tier info card
t = TIER_INFO[tier]
st.markdown(f"""
<div style="background:#0e1420;border:1px solid #1e2d45;border-radius:10px;padding:14px;margin-top:8px">
    <span style="font-size:22px">{t['icon']}</span>
    <strong style="color:#dce8f5;margin-left:8px">{t['label']}</strong>
    <span style="background:#1e2d45;color:#00e5c3;font-size:10px;padding:2px 8px;border-radius:4px;margin-left:8px">
        Weight: {int(t['weight']*100)}%
    </span>
    <p style="color:#5a7090;font-size:12px;margin-top:6px">{t['desc']}</p>
</div>
""", unsafe_allow_html=True)
st.markdown("")

if st.button("💾 Save Profile & Continue →", use_container_width=True):
    if not name or not roll or not college:
        st.error("Please fill all fields.")
    else:
        role_id = get_role_id_by_name(role)
        profile = {
            "student_id":    st.session_state.student_id,
            "name":          name,
            "roll_no":       roll,
            "department":    dept,
            "year":          year,
            "college":       college,
            "college_tier":  tier,
            "cgpa":          cgpa,
            "target_role_id": role_id,
        }
        if save_student_profile(profile):
            st.session_state.student_name   = name
            st.session_state.department     = dept
            st.session_state.target_role_id = role_id
            st.session_state.target_role_name = role
            st.session_state.profile        = profile
            st.success("✅ Profile saved! Go to Skills page next.")
