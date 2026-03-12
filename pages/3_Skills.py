import streamlit as st
from utils.auth import require_login
from utils.domain_relevance import ALL_DOMAINS
from utils.helpers import save_student_profile

require_login()
st.title("📋 Domain-aware Credentials")
st.markdown("Add your projects, certifications, internships and backlogs with domain tags.")
st.markdown("---")

st.info("💡 The domain of each credential is matched against your target role. A Python project boosts a Data Science readiness more than an unrelated one.")

# ── Projects ──
st.subheader("📁 Projects")
if "projects" not in st.session_state:
    st.session_state.projects = [{"title": "", "domain": "General / Other"}]

for i, proj in enumerate(st.session_state.projects):
    c1, c2, c3 = st.columns([3, 2, 0.5])
    st.session_state.projects[i]["title"]  = c1.text_input("Title",  value=proj["title"],  key=f"pt_{i}", label_visibility="collapsed", placeholder="Project title")
    st.session_state.projects[i]["domain"] = c2.selectbox("Domain", ALL_DOMAINS, index=ALL_DOMAINS.index(proj["domain"]), key=f"pd_{i}", label_visibility="collapsed")
    if c3.button("✕", key=f"pr_{i}") and len(st.session_state.projects) > 1:
        st.session_state.projects.pop(i); st.rerun()

if st.button("＋ Add Project"):
    st.session_state.projects.append({"title": "", "domain": "General / Other"}); st.rerun()

st.markdown("---")

# ── Certifications ──
st.subheader("📜 Certifications")
if "certifications" not in st.session_state:
    st.session_state.certifications = [{"name": "", "domain": "General / Other"}]

for i, cert in enumerate(st.session_state.certifications):
    c1, c2, c3 = st.columns([3, 2, 0.5])
    st.session_state.certifications[i]["name"]   = c1.text_input("Name",  value=cert["name"],   key=f"cn_{i}", label_visibility="collapsed", placeholder="Certification name")
    st.session_state.certifications[i]["domain"]  = c2.selectbox("Domain", ALL_DOMAINS, index=ALL_DOMAINS.index(cert["domain"]), key=f"cd_{i}", label_visibility="collapsed")
    if c3.button("✕", key=f"cr_{i}") and len(st.session_state.certifications) > 1:
        st.session_state.certifications.pop(i); st.rerun()

if st.button("＋ Add Certification"):
    st.session_state.certifications.append({"name": "", "domain": "General / Other"}); st.rerun()

st.markdown("---")

# ── Internships ──
st.subheader("🏢 Internships")
if "internships" not in st.session_state:
    st.session_state.internships = [{"company": "", "domain": "General / Other", "months": 2}]

for i, intern in enumerate(st.session_state.internships):
    c1, c2, c3, c4 = st.columns([2, 2, 1, 0.5])
    st.session_state.internships[i]["company"] = c1.text_input("Company", value=intern["company"], key=f"ic_{i}", label_visibility="collapsed", placeholder="Company name")
    st.session_state.internships[i]["domain"]  = c2.selectbox("Domain", ALL_DOMAINS, index=ALL_DOMAINS.index(intern["domain"]), key=f"id_{i}", label_visibility="collapsed")
    st.session_state.internships[i]["months"]  = c3.number_input("Months", min_value=1, max_value=24, value=intern["months"], key=f"im_{i}", label_visibility="collapsed")
    if c4.button("✕", key=f"ir_{i}") and len(st.session_state.internships) > 1:
        st.session_state.internships.pop(i); st.rerun()

if st.button("＋ Add Internship"):
    st.session_state.internships.append({"company": "", "domain": "General / Other", "months": 2}); st.rerun()

st.markdown("---")

# ── Backlogs ──
st.subheader("⚠️ Backlogs")
st.caption("Domain-relevant backlogs are penalised more heavily in the readiness formula.")
if "backlogs" not in st.session_state:
    st.session_state.backlogs = []

for i, bl in enumerate(st.session_state.backlogs):
    c1, c2, c3 = st.columns([3, 2, 0.5])
    st.session_state.backlogs[i]["subject"] = c1.text_input("Subject", value=bl["subject"], key=f"bs_{i}", label_visibility="collapsed", placeholder="Subject name")
    st.session_state.backlogs[i]["domain"]  = c2.selectbox("Domain", ALL_DOMAINS, index=ALL_DOMAINS.index(bl["domain"]), key=f"bd_{i}", label_visibility="collapsed")
    if c3.button("✕", key=f"br_{i}"):
        st.session_state.backlogs.pop(i); st.rerun()

if st.button("＋ Add Backlog"):
    st.session_state.backlogs.append({"subject": "", "domain": "General / Other"}); st.rerun()

st.markdown("---")

if st.button("🔍 Analyze Skill Gap →", use_container_width=True):
    # Save credentials to session state for analysis
    st.session_state.cred_projects       = [p for p in st.session_state.projects       if p.get("title")]
    st.session_state.cred_certifications = [c for c in st.session_state.certifications if c.get("name")]
    st.session_state.cred_internships    = [i for i in st.session_state.internships    if i.get("company")]
    st.session_state.cred_backlogs       = [b for b in st.session_state.backlogs       if b.get("subject")]

    # Update student profile with credential counts
    profile = st.session_state.get("profile", {})
    profile.update({
        "student_id":         st.session_state.student_id,
        "num_projects":       len(st.session_state.cred_projects),
        "project_domains":    ",".join(p["domain"] for p in st.session_state.cred_projects),
        "num_certifications": len(st.session_state.cred_certifications),
        "cert_domains":       ",".join(c["domain"] for c in st.session_state.cred_certifications),
        "num_internships":    len(st.session_state.cred_internships),
        "internship_domains": ",".join(i["domain"] for i in st.session_state.cred_internships),
        "internship_months":  ",".join(str(i["months"]) for i in st.session_state.cred_internships),
        "num_backlogs":       len(st.session_state.cred_backlogs),
        "backlog_domains":    ",".join(b["domain"] for b in st.session_state.cred_backlogs),
    })
    save_student_profile(profile)
    st.success("✅ Credentials saved! Go to Gap Analysis page.")


