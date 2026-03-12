import streamlit as st
import plotly.graph_objects as go
from utils.auth import require_login
from utils.helpers import get_role_skills
from ml.scoring import compute_readiness, save_analysis_to_db
from ml.similarity import cosine_similarity

require_login()
st.title("📈 Progress Tracker")
st.markdown("Re-rate your skills after upskilling and recalculate readiness.")
st.markdown("---")

role_id   = st.session_state.get("target_role_id")
role_name = st.session_state.get("target_role_name","")
profile   = st.session_state.get("profile",{})
orig      = st.session_state.get("skill_scores",{})

if not role_id or not orig:
    st.warning("⚠️ Please complete Profile, Skills and Gap Analysis first.")
    st.stop()

role_skills = get_role_skills(role_id)
st.subheader("✏️ Update Your Skill Levels")
st.caption("Move the sliders to reflect your current skill levels after upskilling.")

updated = {}
cols = st.columns(2)
for i, (skill_name, info) in enumerate(role_skills.items()):
    sk_id = info["skill_id"]
    bench = info["benchmark"]
    orig_val = float(orig.get(sk_id, 0.0))
    new_val  = cols[i%2].slider(
        f"{skill_name} (required: {bench}/10)",
        min_value=0.0, max_value=10.0,
        value=orig_val, step=0.5,
        key=f"prog_{sk_id}"
    )
    updated[sk_id] = new_val

st.markdown("---")

if st.button("🔄 Recalculate Readiness", use_container_width=True):
    new_result = compute_readiness(
        student_scores  = updated,
        role_id         = role_id,
        role_name       = role_name,
        cgpa            = float(profile.get("cgpa",7.5)),
        college_tier    = int(profile.get("college_tier",3)),
        projects        = st.session_state.get("cred_projects",[]),
        certifications  = st.session_state.get("cred_certifications",[]),
        internships     = st.session_state.get("cred_internships",[]),
        backlogs        = st.session_state.get("cred_backlogs",[]),
    )
    new_r   = new_result["readiness_score"]
    orig_r  = st.session_state.get("readiness",0)
    delta   = new_r - orig_r
    new_gaps = len([sk for sk, info in role_skills.items()
                    if updated.get(info["skill_id"],0) < info["benchmark"]])

    c1, c2, c3 = st.columns(3)
    c1.metric("New Readiness",    f"{new_r:.1f}%",  f"{delta:+.1f}% from original")
    c2.metric("Original Score",   f"{orig_r:.1f}%")
    c3.metric("Remaining Gaps",   new_gaps)

    save_analysis_to_db(st.session_state.student_id, role_id, new_r,
                        cosine_similarity(updated, role_id), 0, new_gaps)

    # ── Before vs After Chart ──
    st.markdown("---")
    st.subheader("📊 Before vs After")
    skills_list  = list(role_skills.keys())
    before_vals  = [float(orig.get(role_skills[s]["skill_id"],0)) for s in skills_list]
    after_vals   = [updated.get(role_skills[s]["skill_id"],0) for s in skills_list]
    bench_vals   = [role_skills[s]["benchmark"] for s in skills_list]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Before",    x=skills_list, y=before_vals, marker_color="#ff4560"))
    fig.add_trace(go.Bar(name="After",     x=skills_list, y=after_vals,  marker_color="#00e5c3"))
    fig.add_trace(go.Scatter(name="Required", x=skills_list, y=bench_vals,
                             mode="lines+markers", line=dict(color="#ffc837", dash="dash")))
    fig.update_layout(
        barmode="group", paper_bgcolor="#070b14", plot_bgcolor="#0e1420",
        font_color="#dce8f5", legend=dict(bgcolor="#0e1420"),
        xaxis=dict(gridcolor="#1e2d45"), yaxis=dict(gridcolor="#1e2d45", range=[0,11]),
        height=400, margin=dict(t=20,b=100)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.session_state.skill_scores = updated
    st.success("✅ Progress saved!")
