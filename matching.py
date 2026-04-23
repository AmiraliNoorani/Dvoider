"""Co-founder matching engine — pure functions, no Streamlit imports.

Score = role_fit (0-60) + skill_complementarity (0-30) + stage_category_affinity (0-10).
The breakdown is exposed so the UI can show *why* a match scored what it did.
"""
from __future__ import annotations

# Roles that are "adjacent" to each other — a Backend Engineer is a partial
# match for a CTO slot, a Full-Stack Engineer can fill in for either, etc.
_ADJACENT_ROLES: dict[str, set[str]] = {
    "CTO": {"Backend Engineer", "Full-Stack Engineer", "ML Engineer", "Mobile Engineer"},
    "Backend Engineer": {"CTO", "Full-Stack Engineer"},
    "Full-Stack Engineer": {"Backend Engineer", "CTO"},
    "ML Engineer": {"CTO", "Backend Engineer"},
    "Mobile Engineer": {"CTO", "Full-Stack Engineer"},
    "Designer": {"Product Lead"},
    "Product Lead": {"Designer", "GTM Lead"},
    "GTM Lead": {"Product Lead", "Operations Lead"},
    "Operations Lead": {"GTM Lead"},
    "Clinical Lead": {"Domain Expert"},
    "Domain Expert": {"Clinical Lead", "Learning Scientist"},
    "Learning Scientist": {"Domain Expert"},
    "DevRel Lead": {"GTM Lead", "Product Lead"},
    "Compliance Lead": {"Domain Expert"},
}


def _role_fit(user_role: str, missing_roles: list[str]) -> tuple[int, str]:
    if user_role in missing_roles:
        return 60, f"covers your missing {user_role}"
    for m in missing_roles:
        if user_role in _ADJACENT_ROLES.get(m, set()):
            return 35, f"adjacent fit for {m} ({user_role})"
    return 8, f"role ({user_role}) not in your gap list"


def _skill_complementarity(user_skills: list[str], required_skills: list[str]) -> tuple[int, list[str]]:
    if not required_skills:
        return 0, []
    user_set = {s.lower(): s for s in user_skills}
    overlap_display: list[str] = []
    for req in required_skills:
        # Substring match either direction so "Backend Engineering" matches "Backend".
        rl = req.lower()
        for ul, orig in user_set.items():
            if ul == rl or ul in rl or rl in ul:
                overlap_display.append(orig)
                break
    ratio = len(overlap_display) / len(required_skills)
    score = int(round(ratio * 30))
    return score, overlap_display


def _stage_category_affinity(
    profile_category: str,
    profile_stage: str,
    user_categories: list[str],
    user_stages: list[str],
) -> tuple[int, list[str]]:
    notes: list[str] = []
    score = 0
    if profile_category and profile_category in [c.lower() for c in user_categories]:
        score += 6
        notes.append(f"shipped in {profile_category}")
    if profile_stage and profile_stage in [s.lower() for s in user_stages]:
        score += 4
        notes.append(f"worked at {profile_stage} stage")
    return score, notes


def _build_rationale(
    user: dict,
    role_note: str,
    overlap: list[str],
    affinity_notes: list[str],
) -> str:
    bits = [role_note]
    if overlap:
        shown = overlap[:3]
        bits.append(f"brings {', '.join(shown)}")
    if affinity_notes:
        bits.append(affinity_notes[0])
    track_record = user.get("milestones_shipped", 0)
    if track_record >= 15:
        bits.append(f"{track_record} milestones shipped")
    rationale = "; ".join(bits)
    return rationale[0].upper() + rationale[1:] + "."


def rank_cofounders(profile: dict, users: list[dict], top_n: int = 3) -> list[dict]:
    missing = profile.get("missing_roles", [])
    required = profile.get("required_skills", [])
    cat = profile.get("category", "").lower()
    stage = profile.get("stage", "").lower()

    scored: list[dict] = []
    for u in users:
        role_pts, role_note = _role_fit(u["role"], missing)
        skill_pts, overlap = _skill_complementarity(u.get("skills", []), required)
        aff_pts, aff_notes = _stage_category_affinity(
            cat, stage, u.get("categories", []), u.get("stages_shipped", [])
        )
        # On-time rate as a small reliability tiebreaker (0-2 pts), so two
        # otherwise-equal candidates rank by track record.
        reliability = int(round(u.get("on_time_rate", 0.85) * 2))
        total = role_pts + skill_pts + aff_pts + reliability

        scored.append({
            **u,
            "score": total,
            "score_breakdown": {
                "role_fit": role_pts,
                "skill_complementarity": skill_pts,
                "stage_category_affinity": aff_pts,
                "reliability": reliability,
            },
            "skill_overlap": overlap,
            "rationale": _build_rationale(u, role_note, overlap, aff_notes),
        })

    scored.sort(key=lambda x: (-x["score"], -x.get("milestones_shipped", 0)))
    return scored[:top_n]
