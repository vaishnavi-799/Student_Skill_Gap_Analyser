from utils.auth import init_session, login, signup, logout, require_login
from utils.helpers import (
    get_roles_for_dept,
    get_role_id_by_name,
    get_role_skills,
    get_topics_for_skill,
    save_student_profile,
    save_skill_scores,
    format_pct,
    priority_color
)
from utils.college_tier import get_tier_weight, get_tier_info
from utils.domain_relevance import get_relevance, ALL_DOMAINS