import numpy as np
from config.supabase_client import get_supabase

# ── College tier weights (Requirement 1) ──
TIER_WEIGHT = {1: 1.00, 2: 0.85, 3: 0.70, 4: 0.60, 5: 0.45}

# ── Domain relevance table (Requirement 3) ──
DOMAIN_RELEVANCE = {
    "Python":                {"Data Scientist": 1.0, "ML Engineer": 1.0, "Software Developer": 0.7,
                              "Web Developer": 0.5, "DevOps Engineer": 0.6, "default": 0.3},
    "Machine Learning":      {"Data Scientist": 1.0, "ML Engineer": 1.0, "Software Developer": 0.4, "default": 0.2},
    "Web Development":       {"Web Developer": 1.0, "Software Developer": 0.6, "Product Manager": 0.4, "default": 0.2},
    "Data Analysis":         {"Data Scientist": 0.9, "ML Engineer": 0.7, "Product Manager": 0.5, "default": 0.3},
    "Embedded Systems":      {"Embedded Systems Engineer": 1.0, "IoT Developer": 0.9,
                              "Hardware Design Engineer": 0.7, "VLSI Design Engineer": 0.5, "default": 0.2},
    "VLSI / Chip Design":    {"VLSI Design Engineer": 1.0, "Hardware Design Engineer": 0.7,
                              "Embedded Systems Engineer": 0.4, "default": 0.1},
    "IoT / Wireless":        {"IoT Developer": 1.0, "Embedded Systems Engineer": 0.7,
                              "Telecom Engineer": 0.6, "default": 0.2},
    "Structural / Civil":    {"Structural Engineer": 1.0, "Site Engineer": 0.8,
                              "Construction Manager": 0.7, "default": 0.2},
    "AutoCAD / CAD":         {"Structural Engineer": 0.8, "Site Engineer": 0.9,
                              "Mechanical Design Engineer": 0.9, "Automobile Engineer": 0.7, "default": 0.3},
    "Mechanical Design":     {"Mechanical Design Engineer": 1.0, "Automobile Engineer": 0.8,
                              "Manufacturing Engineer": 0.6, "Robotics Engineer": 0.5, "default": 0.2},
    "Chemical Process":      {"Process Engineer": 1.0, "Petrochemical Engineer": 0.9,
                              "R&D Chemist": 0.5, "default": 0.2},
    "Pharma / Bio":          {"Pharmaceutical Engineer": 1.0, "Quality Assurance Engineer": 0.7,
                              "R&D Chemist": 0.6, "default": 0.2},
    "DevOps / Cloud":        {"DevOps Engineer": 1.0, "ML Engineer": 0.6,
                              "Software Developer": 0.5, "default": 0.2},
    "Networking / Security": {"Cybersecurity Analyst": 1.0, "DevOps Engineer": 0.6,
                              "Telecom Engineer": 0.5, "default": 0.2},
    "Research & Development":{"R&D Chemist": 1.0, "Data Scientist": 0.6,
                              "ML Engineer": 0.5, "default": 0.3},
    "General / Other":       {"default": 0.3},
}


def get_domain_relevance(domain: str, role_name: str) -> float:
    """Return relevance score (0–1) of a domain for a given role."""
    dr = DOMAIN_RELEVANCE.get(domain, {"default": 0.3})
    return dr.get(role_name, dr.get("default", 0.3))


# ══════════════════════════════════════════════════════
#  REQUIREMENT 2 — Topic-weighted skill score
# ══════════════════════════════════════════════════════

def compute_topic_skill_score(topics: list, known_indices: list) -> float:
    """
    topics        : list of dicts  [{"topic_name": ..., "difficulty_weight": 1/2/3}, ...]
    known_indices : list of int    indices the student ticked as known

    Returns skill score on scale 0–10.
    Score = (sum of weights of known topics / sum of all weights) * 10
    """
    if not topics:
        return 0.0
    total_weight = sum(t["difficulty_weight"] for t in topics)
    known_weight = sum(topics[i]["difficulty_weight"] for i in known_indices if i < len(topics))
    return round((known_weight / total_weight) * 10, 2) if total_weight > 0 else 0.0


# ══════════════════════════════════════════════════════
#  GAP COMPUTATION
# ══════════════════════════════════════════════════════

def compute_gaps(student_scores: dict, role_id: str) -> dict:
    """
    student_scores : {skill_id: score (0–10), ...}
    role_id        : e.g. "JR002"

    Returns:
    {
      skill_name: {
        "skill_id":    str,
        "student":     float,
        "required":    int,
        "gap":         float,   # max(0, required - student)
        "surplus":     float,   # max(0, student - required)
        "gap_pct":     float,   # gap as % of required
        "match_pct":   float,   # student/required * 100
      }, ...
    }
    """
    supabase = get_supabase()

    # Fetch role details
    role_resp = supabase.table("job_roles") \
                        .select("*") \
                        .eq("role_id", role_id) \
                        .execute()
    if not role_resp.data:
        raise ValueError(f"Role {role_id} not found in database.")
    role = role_resp.data[0]

    skill_ids  = role["required_skill_ids"].split(",")
    benchmarks = list(map(int, role["benchmark_scores"].split(",")))

    # Fetch skill names
    skills_resp = supabase.table("skills") \
                          .select("skill_id, skill_name") \
                          .in_("skill_id", skill_ids) \
                          .execute()
    skill_name_map = {s["skill_id"]: s["skill_name"] for s in skills_resp.data}

    gaps = {}
    for sk_id, bench in zip(skill_ids, benchmarks):
        skill_name = skill_name_map.get(sk_id, sk_id)
        student    = student_scores.get(sk_id, 0.0)
        gap        = max(0.0, bench - student)
        surplus    = max(0.0, student - bench)
        match_pct  = min(100.0, round((student / bench) * 100, 1)) if bench > 0 else 100.0
        gap_pct    = round((gap / bench) * 100, 1) if bench > 0 else 0.0

        gaps[skill_name] = {
            "skill_id":  sk_id,
            "student":   round(student, 2),
            "required":  bench,
            "gap":       round(gap, 2),
            "surplus":   round(surplus, 2),
            "gap_pct":   gap_pct,
            "match_pct": match_pct,
        }

    return gaps


def get_feature_importance(gaps: dict) -> list:
    """
    Returns skills sorted by gap (most critical first).
    Used for roadmap ordering.
    """
    sorted_gaps = sorted(
        [(skill, info["gap"]) for skill, info in gaps.items() if info["gap"] > 0],
        key=lambda x: x[1],
        reverse=True
    )
    return sorted_gaps
