TIER_WEIGHT = {1: 1.00, 2: 0.85, 3: 0.70, 4: 0.60, 5: 0.45}

TIER_INFO = {
    1: {"label": "Tier 1 — IIT / IISc",           "icon": "🥇", "desc": "Premier national institutes",    "color": "#ffc837", "weight": 1.00},
    2: {"label": "Tier 2 — NIT / BITS / IIIT",    "icon": "🥈", "desc": "Top technical universities",     "color": "#4d9fff", "weight": 0.85},
    3: {"label": "Tier 3 — State Govt University", "icon": "🥉", "desc": "Government universities",        "color": "#00e5c3", "weight": 0.70},
    4: {"label": "Tier 4 — Private Tier-A",        "icon": "🏫", "desc": "Established private colleges",   "color": "#a855f7", "weight": 0.60},
    5: {"label": "Tier 5 — Private Tier-B/C",      "icon": "🏢", "desc": "Other private colleges",         "color": "#ff7b3a", "weight": 0.45},
}

def get_tier_weight(tier: int) -> float:
    return TIER_WEIGHT.get(int(tier), 0.60)

def get_tier_info(tier: int) -> dict:
    return TIER_INFO.get(int(tier), TIER_INFO[3])