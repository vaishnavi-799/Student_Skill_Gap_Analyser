import streamlit as st
from utils.auth import require_login
from utils.helpers import get_role_skills, get_topics_for_skill, save_skill_scores
from ml.gap_engine import compute_topic_skill_score

require_login()

st.title("🛠️ Skill Assessment")
st.caption("Tick only topics you genuinely know. Score is auto-calculated from topic weights.")
st.markdown("---")

role_id = st.session_state.get("target_role_id")
if not role_id:
    st.warning("⚠️ Complete your Profile first.")
    st.stop()

role_skills = get_role_skills(role_id)
if not role_skills:
    st.error("Could not load skills for this role.")
    st.stop()

if "topic_checks" not in st.session_state:
    st.session_state.topic_checks = {}

skill_scores = {}
total_match  = 0
skill_count  = len(role_skills)

for skill_name, info in role_skills.items():
    skill_id = info["skill_id"]
    bench    = info["benchmark"]
    topics   = get_topics_for_skill(skill_id)

    if skill_id not in st.session_state.topic_checks:
        st.session_state.topic_checks[skill_id] = [False] * len(topics)

    known_idx = [i for i, v in enumerate(st.session_state.topic_checks[skill_id]) if v]
    score     = compute_topic_skill_score(topics, known_idx)
    skill_scores[skill_id] = score
    total_match += min(1.0, score / bench) if bench > 0 else 1.0

avg_match = (total_match / skill_count * 100) if skill_count > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Skills to Assess", skill_count)
col2.metric("Avg Coverage",     f"{avg_match:.1f}%")
col3.metric("Target Role",      st.session_state.get("target_role_name", "—"))

st.progress(avg_match / 100, text=f"Overall skill coverage: {avg_match:.1f}%")
st.markdown("---")

for skill_name, info in role_skills.items():
    skill_id = info["skill_id"]
    bench    = info["benchmark"]
    topics   = get_topics_for_skill(skill_id)
    score    = skill_scores[skill_id]
    pct      = int((score / bench) * 100) if bench > 0 else 0
    color    = "🟢" if pct >= 75 else "🟡" if pct >= 40 else "🔴"

    with st.expander(f"{color} **{skill_name}** — {score:.1f}/10  |  Required: {bench}/10  |  Coverage: {pct}%"):
        st.progress(min(pct, 100) / 100)
        if topics:
            st.caption("Tick topics you know:")
            cols = st.columns(3)
            for i, topic in enumerate(topics):
                w_label = {1: "Basic", 2: "Intermediate", 3: "Advanced"}.get(topic["difficulty_weight"], "")
                checked = cols[i % 3].checkbox(
                    f"{topic['topic_name']} ({w_label})",
                    value=st.session_state.topic_checks[skill_id][i],
                    key=f"t_{skill_id}_{i}"
                )
                st.session_state.topic_checks[skill_id][i] = checked
        else:
            st.info("No subtopics defined for this skill.")

st.session_state.skill_scores = skill_scores
st.markdown("---")

if st.button("💾 Save Skills & Go to Credentials →", use_container_width=True):
    scores_list = [
        {
            "skill_id":           sk,
            "skill_score":        sc,
            "topics_known_count": sum(st.session_state.topic_checks.get(sk, []))
        }
        for sk, sc in skill_scores.items()
    ]
    if save_skill_scores(st.session_state.student_id, scores_list):
        st.success("✅ Skills saved! Go to Credentials page from the sidebar.")