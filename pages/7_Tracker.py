import streamlit as st
from datetime import datetime
from utils.auth import require_login
from utils.helpers import priority_color
from config.supabase_client import get_supabase

require_login()
st.title("✅ Upskill Tracker")
st.markdown("Log your daily learning tasks and track progress.")
st.markdown("---")

sid = st.session_state.student_id

def load_tasks():
    try:
        res = get_supabase().table("student_tasks").select("*").eq("student_id", sid).order("created_at", desc=True).execute()
        return res.data or []
    except:
        return []

def add_task(title, skill, priority):
    get_supabase().table("student_tasks").insert({
        "student_id": sid, "title": title, "skill_tag": skill,
        "priority": priority, "is_done": False
    }).execute()

def toggle_task(task_id, current):
    get_supabase().table("student_tasks").update({"is_done": not current}).eq("id", task_id).execute()

def delete_task(task_id):
    get_supabase().table("student_tasks").delete().eq("id", task_id).execute()

tasks = load_tasks()
total = len(tasks)
done  = sum(1 for t in tasks if t["is_done"])
pct   = int(done/total*100) if total > 0 else 0
pend  = total - done

# ── Stats ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tasks",      total)
c2.metric("Completed",        done)
c3.metric("Pending",          pend)
c4.metric("Completion Rate",  f"{pct}%")
st.progress(pct/100, text=f"{pct}% complete")

st.markdown("---")

# ── Add Task ──
st.subheader("➕ Add New Task")
role_id = st.session_state.get("target_role_id")
skill_options = [""]
if role_id:
    from utils.helpers import get_role_skills
    skill_options += list(get_role_skills(role_id).keys())

col1, col2, col3, col4 = st.columns([3,2,1,1])
task_title = col1.text_input("Task",     placeholder="e.g. Complete Binary Trees module", label_visibility="collapsed")
task_skill = col2.selectbox("Skill",     skill_options, label_visibility="collapsed")
task_pri   = col3.selectbox("Priority",  ["high","medium","low"], index=1, label_visibility="collapsed")
if col4.button("Add", use_container_width=True):
    if task_title.strip():
        add_task(task_title.strip(), task_skill, task_pri)
        st.rerun()
    else:
        st.error("Enter a task title.")

st.markdown("---")

# ── Filter ──
filt = st.radio("Filter", ["All","Pending","Completed"], horizontal=True)
filtered = tasks if filt=="All" else [t for t in tasks if (t["is_done"] if filt=="Completed" else not t["is_done"])]

# ── Progress by Skill ──
if tasks:
    st.subheader("📊 Progress by Skill")
    skill_map = {}
    for t in tasks:
        sk = t.get("skill_tag","")
        if not sk: continue
        if sk not in skill_map: skill_map[sk] = {"total":0,"done":0}
        skill_map[sk]["total"] += 1
        if t["is_done"]: skill_map[sk]["done"] += 1
    if skill_map:
        cols = st.columns(min(len(skill_map), 4))
        for i, (sk, d) in enumerate(skill_map.items()):
            p = int(d["done"]/d["total"]*100)
            cols[i%4].metric(sk, f"{d['done']}/{d['total']}", f"{p}%")
    st.markdown("---")

# ── Task List ──
st.subheader(f"📋 Tasks ({len(filtered)})")
if not filtered:
    st.info("No tasks to show.")
else:
    for task in filtered:
        c1, c2, c3 = st.columns([0.5, 8, 1])
        checked = c1.checkbox("", value=task["is_done"], key=f"chk_{task['id']}")
        if checked != task["is_done"]:
            toggle_task(task["id"], task["is_done"]); st.rerun()

        title_style = "text-decoration:line-through;color:#5a7090" if task["is_done"] else "color:#dce8f5"
        pri_dot     = f"<span style='color:{priority_color(task['priority'])}'>●</span>"
        skill_tag   = f"<span style='background:#0e1420;border:1px solid #1e2d45;color:#00e5c3;font-size:10px;padding:1px 7px;border-radius:4px;margin-left:6px'>{task['skill_tag']}</span>" if task.get("skill_tag") else ""
        c2.markdown(f"<span style='{title_style}'>{pri_dot} {task['title']}</span>{skill_tag}", unsafe_allow_html=True)
        if c3.button("✕", key=f"del_{task['id']}"):
            delete_task(task["id"]); st.rerun()
