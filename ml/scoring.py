from sklearn.preprocessing import MinMaxScaler
import numpy as np
from ml.similarity import skill_match_score
from ml.gap_engine import get_domain_relevance, TIER_WEIGHT
from config.supabase_client import get_supabase


def normalize_features(features: list, feature_min: list, feature_max: list) -> list:
    """
    Min-Max normalization.
    Scales each feature to 0–1 range before feeding into ML model.

    features     : raw values  e.g. [7.5, 3, 2, 0, ...]
    feature_min  : min values for each feature
    feature_max  : max values for each feature
    """
    normalized = []
    for val, mn, mx in zip(features, feature_min, feature_max):
        if mx == mn:
            normalized.append(0.0)
        else:
            normalized.append(round((val - mn) / (mx - mn), 4))
    return normalized


# ══════════════════════════════════════════════════════
#  REQUIREMENT 3 — Domain-aware credential scoring
# ══════════════════════════════════════════════════════

def score_credentials(role_name: str,
                      projects: list,
                      certifications: list,
                      internships: list,
                      backlogs: list) -> dict:
    """
    Scores each credential type based on domain relevance to the target role.

    Each list contains dicts like:
      projects       : [{"title": ..., "domain": ...}, ...]
      certifications : [{"name": ..., "domain": ...}, ...]
      internships    : [{"company": ..., "domain": ..., "months": int}, ...]
      backlogs       : [{"subject": ..., "domain": ...}, ...]

    Returns:
    {
      "project_score":    float (0–1),
      "cert_score":       float (0–1),
      "internship_score": float (0–1),
      "backlog_penalty":  float (0–1),
    }
    """

    def avg_relevance(items, domain_key="domain", weight=1.0, months_key=None):
        if not items:
            return 0.0
        scores = []
        for item in items:
            rel = get_domain_relevance(item.get(domain_key, "General / Other"), role_name)
            if months_key:
                # Internship: longer duration = more weight, capped at 6 months
                duration_factor = min(item.get(months_key, 1) / 6, 1.0)
                scores.append(rel * duration_factor * weight)
            else:
                scores.append(rel * weight)
        return round(min(1.0, sum(scores) / len(scores)), 4)

    project_score    = avg_relevance(projects,       weight=1.0)
    cert_score       = avg_relevance(certifications, weight=0.8)
    internship_score = avg_relevance(internships,    weight=1.2, months_key="months")
    backlog_penalty  = avg_relevance(backlogs,       weight=0.9)

    return {
        "project_score":    project_score,
        "cert_score":       cert_score,
        "internship_score": internship_score,
        "backlog_penalty":  backlog_penalty,
    }


# ══════════════════════════════════════════════════════
#  FINAL READINESS FORMULA (Req 1 + Req 2 + Req 3)
# ══════════════════════════════════════════════════════

def compute_readiness(
    student_scores: dict,
    role_id: str,
    role_name: str,
    cgpa: float,
    college_tier: int,
    projects: list,
    certifications: list,
    internships: list,
    backlogs: list
) -> dict:
    """
    Computes the final readiness score (0–100) combining:
      - Topic-weighted skill match     45%  (Req 2)
      - CGPA score                     12%
      - College tier weight            10%  (Req 1)
      - Certification relevance         8%  (Req 3)
      - Project relevance              10%  (Req 3)
      - Internship relevance           10%  (Req 3)
      - Backlog penalty               - 5%  (Req 3)

    Returns dict with final score + each component.
    """
    # Component 1 — Topic-weighted skill match (0–1)
    s_match = skill_match_score(student_scores, role_id)

    # Component 2 — CGPA (0–1)
    cgpa_score = round(min(1.0, cgpa / 10.0), 4)

    # Component 3 — College tier (Req 1)
    tier_score = TIER_WEIGHT.get(int(college_tier), 0.60)

    # Component 4,5,6,7 — Domain-aware credentials (Req 3)
    cred = score_credentials(role_name, projects, certifications, internships, backlogs)

    # Weighted sum → scale to 100
    readiness = (
        s_match                      * 0.45 * 100 +
        cgpa_score                   * 0.12 * 100 +
        tier_score                   * 0.10 * 100 +
        cred["cert_score"]           * 0.08 * 100 +
        cred["project_score"]        * 0.10 * 100 +
        cred["internship_score"]     * 0.10 * 100 -
        cred["backlog_penalty"]      * 0.05 * 100
    )
    readiness = round(min(100.0, max(0.0, readiness)), 2)

    return {
        "readiness_score":      readiness,
        "skill_match_pct":      round(s_match * 100, 2),
        "cgpa_score_pct":       round(cgpa_score * 100, 2),
        "tier_score_pct":       round(tier_score * 100, 2),
        "cert_score_pct":       round(cred["cert_score"] * 100, 2),
        "project_score_pct":    round(cred["project_score"] * 100, 2),
        "internship_score_pct": round(cred["internship_score"] * 100, 2),
        "backlog_penalty_pct":  round(cred["backlog_penalty"] * 100, 2),
    }


def save_analysis_to_db(student_id: str, role_id: str,
                        readiness: float, cosine: float,
                        placement: float, num_gaps: int):
    """Save analysis result back to Supabase student_analysis table."""
    supabase = get_supabase()
    supabase.table("student_analysis").upsert({
        "student_id":            student_id,
        "role_id":               role_id,
        "readiness_score":       readiness,
        "cosine_similarity":     cosine,
        "placement_probability": placement,
        "num_skill_gaps":        num_gaps,
    }).execute()
