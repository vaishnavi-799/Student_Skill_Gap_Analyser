import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.auth import require_login
from ml.gap_engine import compute_gaps
from ml.similarity import cosine_similarity, skill_match_score
from ml.scoring import compute_readiness, save_analysis_to_db
from ml.recommender import generate_roadmap
from ml.placement_model import predict_placement

require_login()
st.title("📊 Skill Gap Analysis")
st.markdown("---")

role_id   = st.session_state.get("target_role_id")
role_name = st.session_state.get("target_role_name", "")
profile   = st.session_state.get("profile", {})
scores    = st.session_state.get("skill_scores", {})

if not role_id or not scores:
    st.warning("⚠️ Please complete Profile and Skills pages first.")
    st.stop()

# ── Run ML ──
if st.button("🔍 Run Analysis", use_container_width=True) or st.session_state.get("analysis_done"):
    with st.spinner("Running ML analysis..."):
        gaps    = compute_gaps(scores, role_id)
        cosine  = cosine_similarity(scores, role_id)
        sm      = skill_match_score(scores, role_id)

        result  = compute_readiness(
            student_scores  = scores,
            role_id         = role_id,
            role_name       = role_name,
            cgpa            = float(profile.get("cgpa", 7.5)),
            college_tier    = int(profile.get("college_tier", 3)),
            projects        = st.session_state.get("cred_projects", []),
            certifications  = st.session_state.get("cred_certifications", []),
            internships     = st.session_state.get("cred_internships", []),
            backlogs        = st.session_state.get("cred_backlogs", []),
        )
        readiness  = result["readiness_score"]
        num_gaps   = len([g for g in gaps.values() if g["gap"] > 0])

        placement = predict_placement(
            skill_match_score         = sm,
            cosine_similarity         = cosine,
            cgpa                      = float(profile.get("cgpa", 7.5)),
            college_tier              = int(profile.get("college_tier", 3)),
            project_relevance_score   = result["project_score_pct"] / 100,
            cert_relevance_score      = result["cert_score_pct"] / 100,
            internship_relevance_score= result["internship_score_pct"] / 100,
            backlog_penalty_score     = result["backlog_penalty_pct"] / 100,
            num_skill_gaps            = num_gaps,
            readiness_score           = readiness,
        )

        roadmap = generate_roadmap(scores, role_id, role_name)

        st.session_state.gap_result      = gaps
        st.session_state.readiness       = readiness
        st.session_state.cosine          = cosine
        st.session_state.placement       = placement
        st.session_state.roadmap         = roadmap
        st.session_state.score_breakdown = result
        st.session_state.analysis_done   = True

        save_analysis_to_db(st.session_state.student_id, role_id, readiness, cosine, placement, num_gaps)

    # ── KPIs ──
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎯 Readiness Score",   f"{readiness:.1f}%")
    c2.metric("📐 Cosine Similarity", f"{cosine*100:.1f}%")
    c3.metric("🏢 Placement Chance",  f"{placement*100:.1f}%")
    c4.metric("❌ Skill Gaps",        num_gaps)

    st.markdown("---")

    # ── Score Breakdown ──
    st.subheader("🔬 Score Breakdown")
    bd = result
    b1,b2,b3 = st.columns(3)
    b1.metric("Skills (45%)",         f"{bd['skill_match_pct']:.1f}%")
    b2.metric("CGPA (12%)",           f"{bd['cgpa_score_pct']:.1f}%")
    b3.metric("College Tier (10%)",   f"{bd['tier_score_pct']:.1f}%")
    b4,b5,b6 = st.columns(3)
    b4.metric("Projects (10%)",       f"{bd['project_score_pct']:.1f}%")
    b5.metric("Internships (10%)",    f"{bd['internship_score_pct']:.1f}%")
    b6.metric("Certifications (8%)",  f"{bd['cert_score_pct']:.1f}%")
    if bd["backlog_penalty_pct"] > 0:
        st.metric("⚠️ Backlog Penalty (-5%)", f"-{bd['backlog_penalty_pct']:.1f}%")

    st.markdown("---")

    # ── Charts ──
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("📡 Skill Radar")
        skill_names = list(gaps.keys())
        student_v   = [gaps[s]["student"]  for s in skill_names]
        bench_v     = [gaps[s]["required"] for s in skill_names]
        labels_short = [s[:12]+"…" if len(s)>12 else s for s in skill_names]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=bench_v,   theta=labels_short, fill="toself",
                      name="Benchmark", line_color="#00e5c3", fillcolor="rgba(0,229,195,0.1)"))
        fig.add_trace(go.Scatterpolar(r=student_v, theta=labels_short, fill="toself",
                      name="Your Skills", line_color="#4d9fff", fillcolor="rgba(77,159,255,0.15)"))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,10],gridcolor="#1e2d45"),
                          bgcolor="#0e1420"), paper_bgcolor="#070b14", font_color="#dce8f5",
                          legend=dict(bgcolor="#0e1420"), height=350, margin=dict(t=20,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.subheader("🎯 Readiness Gauge")
        gauge = go.Figure(go.Indicator(
            mode  = "gauge+number",
            value = readiness,
            domain = {"x":[0,1],"y":[0,1]},
            title  = {"text":"Readiness %","font":{"color":"#dce8f5"}},
            number = {"suffix":"%","font":{"color":"#00e5c3","size":36}},
            gauge  = {
                "axis":  {"range":[0,100],"tickcolor":"#5a7090"},
                "bar":   {"color":"#00e5c3"},
                "bgcolor":"#0e1420",
                "steps": [{"range":[0,40],"color":"rgba(255,69,96,0.2)"},
                           {"range":[40,70],"color":"rgba(255,200,55,0.2)"},
                           {"range":[70,100],"color":"rgba(0,229,195,0.15)"}],
                "threshold":{"line":{"color":"white","width":3},"value":70},
            }
        ))
        gauge.update_layout(paper_bgcolor="#070b14", font_color="#dce8f5", height=300, margin=dict(t=30,b=10))
        st.plotly_chart(gauge, use_container_width=True)

        label = ("🟢 Highly Ready" if readiness>=70 else "🟡 Moderately Ready" if readiness>=50 else "🔴 Significant Gaps")
        st.markdown(f"<div style='text-align:center;font-size:14px;color:#dce8f5'>{label}</div>", unsafe_allow_html=True)
        st.progress(placement, text=f"Placement Probability: {placement*100:.1f}%")

    st.markdown("---")

    # ── Gap Table ──
    st.subheader("🔍 Skill-by-Skill Breakdown")
    rows = []
    for skill, info in gaps.items():
        status = "✅ Met" if info["gap"]==0 else "⚠️ Close" if info["gap"]<=2 else "❌ Gap"
        rows.append({
            "Skill":       skill,
            "Your Score":  f"{info['student']:.1f}/10",
            "Required":    f"{info['required']}/10",
            "Gap":         f"-{info['gap']:.1f}" if info["gap"]>0 else f"+{info['surplus']:.1f}",
            "Match":       f"{info['match_pct']}%",
            "Status":      status,
        })
    st.dataframe(rows, use_container_width=True, hide_index=True)
