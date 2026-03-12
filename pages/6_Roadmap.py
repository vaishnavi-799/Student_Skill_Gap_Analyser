import streamlit as st
from utils.auth import require_login

require_login()
st.title("🚀 Personalized Upskilling Roadmap")
st.markdown("Priority-ranked by gap severity and domain relevance.")
st.markdown("---")

roadmap = st.session_state.get("roadmap", [])
if not roadmap:
    st.warning("⚠️ Please run Gap Analysis first.")
    st.stop()

total_weeks = sum(r["weeks"] for r in roadmap)
c1, c2, c3 = st.columns(3)
c1.metric("Skills to Upskill", len(roadmap))
c2.metric("Est. Total Weeks",  total_weeks)
c3.metric("Target Readiness",  "85%")

st.markdown("---")

PRIORITY_COLOR = {"High": "#ff4560", "Medium": "#ffc837", "Low": "#00e5c3"}
PLATFORM_COLOR = {"Coursera":"#0056d2","Udemy":"#a435f0","Kaggle":"#20beff",
                  "freeCodeCamp":"#006400","NPTEL":"#e87722","NPTEL / Udemy":"#e87722"}

for item in roadmap:
    pc = PRIORITY_COLOR.get(item["priority_label"], "#5a7090")
    st.markdown(f"""
<div style="background:#0e1420;border:1px solid #1e2d45;border-left:4px solid {pc};
     border-radius:12px;padding:16px;margin-bottom:12px">
  <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
    <span style="background:{pc}22;color:{pc};border:1px solid {pc};font-size:10px;
          font-family:monospace;padding:2px 8px;border-radius:10px">
      #{item['priority']} {item['priority_label'].upper()} PRIORITY
    </span>
    <strong style="color:#dce8f5;font-size:15px">{item['skill']}</strong>
    <span style="background:#1e2d45;color:#ff4560;font-size:10px;font-family:monospace;
          padding:2px 8px;border-radius:10px">gap: {item['gap']:.1f}</span>
  </div>
  <div style="color:#5a7090;font-size:12px;margin-bottom:8px">
    Your score: <strong style="color:#4d9fff">{item['student']:.1f}/10</strong> →
    Required: <strong style="color:#00e5c3">{item['required']}/10</strong> |
    Start: Week {item['week_start']}
  </div>
  <div style="color:#dce8f5;font-size:13px">📚 <a href="{item['url']}" target="_blank"
       style="color:#4d9fff">{item['name']}</a></div>
  <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap">
    <span style="background:#151d2e;border:1px solid #1e2d45;color:{PLATFORM_COLOR.get(item['platform'],'#5a7090')};
          font-size:10px;font-family:monospace;padding:2px 8px;border-radius:4px">
      🎓 {item['platform']}
    </span>
    <span style="background:#151d2e;border:1px solid #1e2d45;color:#5a7090;
          font-size:10px;font-family:monospace;padding:2px 8px;border-radius:4px">
      ⏱ {item['weeks']} week{'s' if item['weeks']>1 else ''}
    </span>
    <span style="background:#151d2e;border:1px solid #1e2d45;color:#5a7090;
          font-size:10px;font-family:monospace;padding:2px 8px;border-radius:4px">
      🗓 Week {item['week_start']}–{item['week_start']+item['weeks']-1}
    </span>
  </div>
</div>
""", unsafe_allow_html=True)
