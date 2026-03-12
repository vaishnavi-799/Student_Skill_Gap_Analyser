import numpy as np
from sklearn.neighbors import NearestNeighbors
from ml.gap_engine import compute_gaps, get_feature_importance
from config.supabase_client import get_supabase

COURSES_DB = {
    # CSE
    "Data Structures":          {"name": "Data Structures & Algorithms",        "platform": "Coursera",      "weeks": 8,  "url": "https://www.coursera.org/specializations/data-structures-algorithms"},
    "Algorithms":               {"name": "Algorithms Specialization",           "platform": "Coursera",      "weeks": 12, "url": "https://www.coursera.org/specializations/algorithms"},
    "OOP Concepts":             {"name": "OOP with Java",                       "platform": "Coursera",      "weeks": 4,  "url": "https://www.coursera.org/learn/object-oriented-java"},
    "DBMS":                     {"name": "Database Management Systems",         "platform": "NPTEL",         "weeks": 6,  "url": "https://nptel.ac.in/courses/106105175"},
    "OS Concepts":              {"name": "Operating Systems",                   "platform": "NPTEL",         "weeks": 8,  "url": "https://nptel.ac.in/courses/106105214"},
    "Computer Networks":        {"name": "Computer Networking",                 "platform": "Coursera",      "weeks": 6,  "url": "https://www.coursera.org/learn/computer-networking"},
    "Python":                   {"name": "Python Bootcamp",                     "platform": "Udemy",         "weeks": 4,  "url": "https://www.udemy.com/course/complete-python-bootcamp"},
    "Machine Learning":         {"name": "ML Specialization",                   "platform": "Coursera",      "weeks": 12, "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
    "Deep Learning":            {"name": "Deep Learning Specialization",        "platform": "Coursera",      "weeks": 16, "url": "https://www.coursera.org/specializations/deep-learning"},
    "Statistics & Probability": {"name": "Statistics with Python",              "platform": "Coursera",      "weeks": 6,  "url": "https://www.coursera.org/specializations/statistics-with-python"},
    "SQL":                      {"name": "SQL for Data Science",                "platform": "Coursera",      "weeks": 2,  "url": "https://www.coursera.org/learn/sql-for-data-science"},
    "Data Visualization":       {"name": "Data Viz with Python",                "platform": "Udemy",         "weeks": 2,  "url": "https://www.udemy.com/course/data-visualization-with-python"},
    "Data Wrangling":           {"name": "Data Wrangling with Pandas",          "platform": "Kaggle",        "weeks": 2,  "url": "https://www.kaggle.com/learn/pandas"},
    "HTML/CSS":                 {"name": "Responsive Web Design",               "platform": "freeCodeCamp",  "weeks": 4,  "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design"},
    "JavaScript":               {"name": "JavaScript Algorithms & DS",          "platform": "freeCodeCamp",  "weeks": 4,  "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures"},
    "React/Vue":                {"name": "React — The Complete Guide",          "platform": "Udemy",         "weeks": 6,  "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux"},
    "Node.js":                  {"name": "Node.js — The Complete Guide",        "platform": "Udemy",         "weeks": 5,  "url": "https://www.udemy.com/course/nodejs-the-complete-guide"},
    "Docker":                   {"name": "Docker & Kubernetes Bootcamp",        "platform": "Udemy",         "weeks": 4,  "url": "https://www.udemy.com/course/docker-kubernetes-the-practical-guide"},
    "Linux/Unix":               {"name": "Linux Command Line Basics",           "platform": "Udemy",         "weeks": 2,  "url": "https://www.udemy.com/course/linux-command-line-volume1"},
    "Version Control":          {"name": "Git & GitHub Crash Course",           "platform": "Udemy",         "weeks": 1,  "url": "https://www.udemy.com/course/git-and-github-bootcamp"},
    "System Design":            {"name": "System Design for Interviews",        "platform": "Udemy",         "weeks": 4,  "url": "https://www.udemy.com/course/system-design-interview-prep"},
    # ECE
    "C/C++ Programming":        {"name": "Embedded C Programming",             "platform": "Udemy",         "weeks": 4,  "url": "https://www.udemy.com/course/embedded-c-programming-design-patterns"},
    "Microcontrollers":         {"name": "ARM Cortex-M Microcontrollers",      "platform": "Udemy",         "weeks": 6,  "url": "https://www.udemy.com/course/microcontroller-embedded-c-programming"},
    "VLSI Design":              {"name": "VLSI Design Flow",                   "platform": "Coursera",      "weeks": 8,  "url": "https://www.coursera.org/learn/vlsi-cad-logic"},
    "Verilog/VHDL":             {"name": "HDL Design with Verilog",            "platform": "Udemy",         "weeks": 4,  "url": "https://www.udemy.com/course/verilog-hdl"},
    "Circuit Design":           {"name": "Analog & Digital Circuits",          "platform": "NPTEL",         "weeks": 6,  "url": "https://nptel.ac.in/courses/108105132"},
    "Signal Processing":        {"name": "Digital Signal Processing",          "platform": "Coursera",      "weeks": 6,  "url": "https://www.coursera.org/learn/dsp"},
    "MATLAB":                   {"name": "MATLAB for Engineers",               "platform": "Coursera",      "weeks": 4,  "url": "https://www.coursera.org/learn/matlab"},
    # MECH
    "CAD (SolidWorks/AutoCAD)": {"name": "SolidWorks Masterclass",            "platform": "Udemy",         "weeks": 4,  "url": "https://www.udemy.com/course/solidworks-for-beginners-part-design"},
    "FEA (ANSYS)":              {"name": "ANSYS FEA for Beginners",            "platform": "Udemy",         "weeks": 3,  "url": "https://www.udemy.com/course/ansys-workbench-fea"},
    "Thermodynamics":           {"name": "Engineering Thermodynamics",         "platform": "NPTEL",         "weeks": 6,  "url": "https://nptel.ac.in/courses/112104113"},
    "Strength of Materials":    {"name": "Mechanics of Materials",             "platform": "Coursera",      "weeks": 6,  "url": "https://www.coursera.org/learn/mechanics-of-materials-i-fundamentals"},
    "Fluid Mechanics":          {"name": "Fluid Mechanics Fundamentals",       "platform": "NPTEL",         "weeks": 6,  "url": "https://nptel.ac.in/courses/112104114"},
    "Manufacturing Processes":  {"name": "Manufacturing Process Technology",   "platform": "NPTEL",         "weeks": 8,  "url": "https://nptel.ac.in/courses/112107077"},
    # CIVIL
    "Structural Analysis":      {"name": "Structural Analysis with STAAD",     "platform": "Udemy",         "weeks": 4,  "url": "https://www.udemy.com/course/staad-pro-training"},
    "RCC Design":               {"name": "RCC Design as per IS Code",          "platform": "Udemy",         "weeks": 3,  "url": "https://www.udemy.com/course/rcc-design"},
    "AutoCAD/STAAD Pro":        {"name": "AutoCAD 2024 Complete Course",       "platform": "Udemy",         "weeks": 3,  "url": "https://www.udemy.com/course/autocad-2d-and-3d-practice-drawings"},
    "Soil Mechanics":           {"name": "Geotechnical Engineering",           "platform": "NPTEL",         "weeks": 6,  "url": "https://nptel.ac.in/courses/105101009"},
    # CHEM
    "Chemical Process Design":  {"name": "Chemical Process Design",            "platform": "Coursera",      "weeks": 6,  "url": "https://www.coursera.org/learn/chemical-engineering"},
    "Process Simulation (Aspen)":{"name": "Aspen Plus for Beginners",          "platform": "Udemy",         "weeks": 3,  "url": "https://www.udemy.com/course/aspen-plus"},
    "Safety & HAZOP":           {"name": "Process Safety Management",          "platform": "Coursera",      "weeks": 4,  "url": "https://www.coursera.org/learn/process-safety"},
    "Organic Chemistry":        {"name": "Organic Chemistry Basics",           "platform": "Coursera",      "weeks": 6,  "url": "https://www.coursera.org/learn/organic-chemistry"},
}


def generate_roadmap(student_scores: dict, role_id: str, role_name: str) -> list:
    """
    Generates a priority-ranked upskilling roadmap based on gap severity.

    Returns list of dicts:
    [
      {
        "priority":    int,
        "skill":       str,
        "gap":         float,
        "student":     float,
        "required":    int,
        "name":        str,   # course name
        "platform":    str,
        "weeks":       int,
        "url":         str,
        "week_start":  int,   # cumulative start week
        "priority_label": str  # High / Medium / Low
      }, ...
    ]
    """
    gaps = compute_gaps(student_scores, role_id)
    ranked = get_feature_importance(gaps)  

    roadmap = []
    week_cursor = 1

    for priority, (skill_name, gap_val) in enumerate(ranked, start=1):
        info     = gaps[skill_name]
        course   = COURSES_DB.get(skill_name, {
            "name":     f"Learn {skill_name}",
            "platform": "NPTEL / Udemy",
            "weeks":    3,
            "url":      "https://nptel.ac.in",
        })

        if gap_val >= 4:
            priority_label = "High"
        elif gap_val >= 2:
            priority_label = "Medium"
        else:
            priority_label = "Low"

        roadmap.append({
            "priority":       priority,
            "skill":          skill_name,
            "gap":            gap_val,
            "student":        info["student"],
            "required":       info["required"],
            "match_pct":      info["match_pct"],
            "name":           course["name"],
            "platform":       course["platform"],
            "weeks":          course["weeks"],
            "url":            course["url"],
            "week_start":     week_cursor,
            "priority_label": priority_label,
        })
        week_cursor += course["weeks"]

    return roadmap


def knn_recommend(student_scores: dict, role_id: str, k: int = 3) -> list:
    """
    KNN-based recommender:
    Finds k past students with similar gap profiles from Supabase
    and returns their most successful upskilling courses.

    Falls back to gap-based roadmap if not enough data in DB.
    """
    supabase = get_supabase()

    try:
        resp = supabase.table("student_skill_scores") \
                       .select("student_id, skill_id, skill_score") \
                       .execute()
        if not resp.data or len(resp.data) < k:
            return generate_roadmap(student_scores, role_id, "")

        role_resp = supabase.table("job_roles") \
                            .select("required_skill_ids, benchmark_scores") \
                            .eq("role_id", role_id) \
                            .execute()
        role      = role_resp.data[0]
        skill_ids = role["required_skill_ids"].split(",")

        from collections import defaultdict
        student_map = defaultdict(dict)
        for row in resp.data:
            student_map[row["student_id"]][row["skill_id"]] = row["skill_score"]

        student_ids = list(student_map.keys())
        X = np.array([
            [student_map[sid].get(sk, 0.0) for sk in skill_ids]
            for sid in student_ids
        ])

        query = np.array([student_scores.get(sk, 0.0) for sk in skill_ids]).reshape(1, -1)

        knn = NearestNeighbors(n_neighbors=min(k, len(student_ids)), metric="euclidean")
        knn.fit(X)
        distances, indices = knn.kneighbors(query)

        similar_students = [student_ids[i] for i in indices[0]]
        return similar_students  

    except Exception:
        return generate_roadmap(student_scores, role_id, "")
