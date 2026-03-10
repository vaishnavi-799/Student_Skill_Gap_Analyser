import numpy as np
from config.supabase_client import get_supabase


def cosine_similarity(student_scores: dict, role_id: str) -> float:
    """
    Measures how closely the student's skill profile SHAPE
    matches the role benchmark — not just raw totals.

    student_scores : {skill_id: score (0–10), ...}
    role_id        : e.g. "JR002"

    Returns float between 0.0 (no match) and 1.0 (perfect match).
    """
    supabase = get_supabase()

    role_resp = supabase.table("job_roles") \
                        .select("required_skill_ids, benchmark_scores") \
                        .eq("role_id", role_id) \
                        .execute()
    if not role_resp.data:
        raise ValueError(f"Role {role_id} not found.")

    role       = role_resp.data[0]
    skill_ids  = role["required_skill_ids"].split(",")
    benchmarks = list(map(int, role["benchmark_scores"].split(",")))

    # Build vectors
    sv = np.array([student_scores.get(sk, 0.0) for sk in skill_ids], dtype=float)
    bv = np.array(benchmarks, dtype=float)

    dot    = np.dot(sv, bv)
    mag_sv = np.linalg.norm(sv)
    mag_bv = np.linalg.norm(bv)

    if mag_sv == 0 or mag_bv == 0:
        return 0.0

    return round(float(dot / (mag_sv * mag_bv)), 4)


def euclidean_distance(student_scores: dict, role_id: str) -> float:
    """
    Euclidean distance between student vector and benchmark vector.
    Lower = closer to role requirement.
    Used internally by KNN recommender.
    """
    supabase = get_supabase()

    role_resp = supabase.table("job_roles") \
                        .select("required_skill_ids, benchmark_scores") \
                        .eq("role_id", role_id) \
                        .execute()
    if not role_resp.data:
        return float("inf")

    role       = role_resp.data[0]
    skill_ids  = role["required_skill_ids"].split(",")
    benchmarks = list(map(int, role["benchmark_scores"].split(",")))

    sv = np.array([student_scores.get(sk, 0.0) for sk in skill_ids], dtype=float)
    bv = np.array(benchmarks, dtype=float)

    return round(float(np.linalg.norm(sv - bv)), 4)


def skill_match_score(student_scores: dict, role_id: str) -> float:
    """
    Average of (student_score / required_score) across all skills.
    Returns value between 0.0 and 1.0.
    Used in readiness formula as skill_match component.
    """
    supabase = get_supabase()

    role_resp = supabase.table("job_roles") \
                        .select("required_skill_ids, benchmark_scores") \
                        .eq("role_id", role_id) \
                        .execute()
    if not role_resp.data:
        return 0.0

    role       = role_resp.data[0]
    skill_ids  = role["required_skill_ids"].split(",")
    benchmarks = list(map(int, role["benchmark_scores"].split(",")))

    ratios = [
        min(1.0, student_scores.get(sk, 0.0) / bench)
        for sk, bench in zip(skill_ids, benchmarks)
        if bench > 0
    ]
    return round(sum(ratios) / len(ratios), 4) if ratios else 0.0
