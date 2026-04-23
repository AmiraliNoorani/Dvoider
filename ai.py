"""Idea-structuring brain.

Two backends, same JSON contract:
  - `_structure_via_openai`: live call to gpt-4o-mini in JSON-object mode
  - `_structure_via_mock`: deterministic keyword-driven heuristic so the
    investor demo runs reliably without a network or API key.

`structure_idea()` prefers live when an api_key is given but always falls
back to mock on any failure — the pitch must never break.
"""
from __future__ import annotations

import json
import os
import re
from typing import Optional

CATEGORIES = ["fintech", "healthtech", "devtools", "consumer", "climate", "b2b saas", "legaltech", "edtech", "music"]
STAGES = ["idea", "prototype", "launched"]

SYSTEM_PROMPT = """You are Dvoider's Architect — you turn a founder's or creator's raw, messy idea into a structured Project Profile.

Return a single JSON object with EXACTLY these keys:
  "one_liner":       string — a punchy one-sentence pitch (<= 18 words)
  "problem":         string — the underlying problem or brief in 1-2 sentences
  "target_user":     string — who the product or piece is for (audience, customer, venue, etc.)
  "category":        string — one of: fintech, healthtech, devtools, consumer, climate, b2b saas, legaltech, edtech, music
  "stage":           string — one of: idea, prototype, launched
  "required_skills": array of 4-7 short strings (e.g. "Python", "Carbon Markets", "Violin")
  "missing_roles":   array of 2-4 short role titles the creator needs (e.g. "CTO", "Clinical Lead", "Violinist")
  "advice":          array of 2-4 short, concrete suggestions to improve or de-risk the idea — each a single actionable sentence (e.g. "Trim duration from 12 to 8 minutes to fit the Cannes festival entry window", "Validate the clinical workflow with 5 practicing clinicians before writing code")

Be specific. Skills should reflect what the build actually needs. Missing roles should be ones the creator explicitly says they lack OR roles obviously unfilled. Advice should be pragmatic tweaks to scope, timing, or approach — not vague platitudes.
Do not include any text outside the JSON object."""


# ---------- Public API ----------

def structure_idea(raw: str, api_key: Optional[str] = None) -> tuple[dict, str]:
    """Returns (profile_dict, source) where source is 'live' or 'mock'."""
    raw = (raw or "").strip()
    if not raw:
        raise ValueError("Idea text is empty.")

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if key:
        try:
            return _structure_via_openai(raw, key), "live"
        except Exception:
            # Pitch-safe: never crash. Fall through to the mock.
            return _structure_via_mock(raw), "mock-fallback"
    return _structure_via_mock(raw), "mock"


# ---------- OpenAI path ----------

def _structure_via_openai(raw: str, api_key: str) -> dict:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Founder's raw idea:\n\n{raw}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.4,
        max_tokens=600,
    )
    data = json.loads(resp.choices[0].message.content)
    return _normalize(data, raw)


# ---------- Mock path ----------

# Keyword → category. Order matters: more specific keywords first.
_CATEGORY_KEYWORDS: list[tuple[str, list[str]]] = [
    ("music", ["violin", "violinist", "cellist", "composer", "orchestral", "symphony", "string quartet", "arrangement", "producer", "song", "album", "studio session", "film score", "ensemble", "sheet music"]),
    ("legaltech", ["contract", "legal", "lawyer", "redline", "clause", "litigation"]),
    ("healthtech", ["medical", "clinical", "patient", "doctor", "med student", "emr", "hipaa", "health"]),
    ("climate", ["carbon", "climate", "emission", "esg", "csrd", "sustain", "green"]),
    ("fintech", ["pos", "payment", "credit", "loan", "lending", "bank", "fintech", "money", "wallet", "payroll", "ledger"]),
    ("edtech", ["tutor", "student", "learn", "exam", "curriculum", "course", "study"]),
    ("devtools", ["api", "developer", "sdk", "ci/cd", "observability", "framework", "ide"]),
    ("consumer", ["consumer", "social", "fan", "marketplace", "retail", "shopper"]),
    ("b2b saas", ["saas", "b2b", "workflow", "team", "enterprise", "ops"]),
]

_CATEGORY_SKILLS: dict[str, list[str]] = {
    "fintech": ["Payments", "Compliance", "Postgres", "Backend Engineering", "Risk Modeling"],
    "healthtech": ["Clinical Workflows", "HIPAA", "Medical Education", "Content", "Backend Engineering"],
    "devtools": ["Distributed Systems", "DX", "TypeScript", "APIs", "Observability"],
    "consumer": ["Mobile", "Brand", "Growth", "Lifecycle", "Design"],
    "climate": ["Carbon Markets", "ESG Reporting", "Verification", "Policy", "Backend Engineering"],
    "b2b saas": ["Sales", "Workflow Design", "Backend Engineering", "Pricing", "Onboarding"],
    "legaltech": ["Contracts", "Real-time Collaboration", "TypeScript", "LLMs", "Workflow Design"],
    "edtech": ["Adaptive Learning", "Curriculum", "LLMs", "Evals", "Content"],
    "music": ["Violin", "Studio Recording", "Sight Reading", "Arrangement", "Music Theory"],
}

_CATEGORY_ROLES: dict[str, list[str]] = {
    "fintech": ["CTO", "Compliance Lead", "GTM Lead"],
    "healthtech": ["Clinical Lead", "ML Engineer", "Designer"],
    "devtools": ["CTO", "Designer", "DevRel Lead"],
    "consumer": ["Designer", "Mobile Engineer", "GTM Lead"],
    "climate": ["Domain Expert", "Backend Engineer", "GTM Lead"],
    "b2b saas": ["GTM Lead", "Product Lead", "Backend Engineer"],
    "legaltech": ["Product Lead", "Full-Stack Engineer", "Domain Expert"],
    "edtech": ["Learning Scientist", "Full-Stack Engineer", "Designer"],
    "music": ["Violinist", "Audio Engineer", "Composer"],
}

_CATEGORY_ADVICE: dict[str, list[str]] = {
    "fintech": [
        "Narrow to one regulatory jurisdiction for v1 — licensing timelines will otherwise dominate your roadmap.",
        "Partner with a licensed payments provider instead of pursuing money-transmitter status yourself.",
        "Define your fraud tolerance and unit economics before any GTM push.",
    ],
    "healthtech": [
        "Validate the clinical workflow with 5 practicing clinicians before writing a line of code.",
        "Decide early whether you'll pursue FDA clearance — it shapes everything downstream.",
        "Build HIPAA-ready infrastructure from day one; retrofitting is painful.",
    ],
    "devtools": [
        "Ship a 500-line ‘hello world’ demo before the full SDK — it's the fastest way to pressure-test DX.",
        "Pick one language ecosystem for v1; cross-stack support triples your maintenance burden.",
        "Open-source the client and charge for the hosted plane — devs won't install closed binaries.",
    ],
    "consumer": [
        "Get 50 weekly actives before building monetization — retention, not revenue, is the only question at this stage.",
        "Launch on one platform first; native-feel beats cross-platform parity for consumer adoption.",
        "Invest in brand on day one — consumer products die in the commodity middle.",
    ],
    "climate": [
        "Pick one regulatory regime (CSRD, SEC, TCFD) as your wedge — ‘all frameworks’ is an integration nightmare.",
        "Line up a verification partner early; auditable data is the moat, not the UI.",
        "Target finance teams, not sustainability teams — they hold the budget.",
    ],
    "b2b saas": [
        "Charge from day one — free pilots with enterprise logos are a trap that delays real product signal.",
        "Pick one ICP and one workflow; horizontal SaaS rarely crosses the chasm from a standing start.",
        "Design for the buyer, not just the user — procurement, security review, and SSO kill deals.",
    ],
    "legaltech": [
        "Anchor on one practice area (M&A, employment, commercial) — lawyers won't trust a generalist tool.",
        "Add audit-trail and version history before AI features; attorneys care more about defensibility than cleverness.",
        "Price per matter or per seat, not per token — lawyers hate variable costs.",
    ],
    "edtech": [
        "Run a 2-week pilot with real learners before scaling content generation — engagement signal dies fast in EdTech.",
        "Partner with one institution for distribution; direct-to-student CAC is brutal.",
        "Build assessment depth before breadth — mastery tracking is what parents and schools pay for.",
    ],
    "music": [
        "Consider trimming the piece to 6–8 minutes — most festival shortlists cap entries around 10.",
        "Record a 2-violin mockup before booking the full 8-piece session to test the arrangement.",
        "Scout players from local conservatories and session-musician networks in your target city.",
        "Lock the tempo and key choices before the session — studio time is your most expensive variable.",
    ],
}

# Phrases that suggest the founder explicitly LACKS a role. Each entry maps a
# regex to the role the mock should add to missing_roles.
_LACK_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bno\s+(clinical|medical|doctor|md)\b", re.I), "Clinical Lead"),
    (re.compile(r"\bno\s+(design|designer)\b", re.I), "Designer"),
    (re.compile(r"\bno\s+(engineering|engineer|technical|build|builder|cto)\b", re.I), "CTO"),
    (re.compile(r"\bnot\s+a\s+(builder|engineer)\b", re.I), "CTO"),
    (re.compile(r"\bno\s+(gtm|sales|growth|marketing)\b", re.I), "GTM Lead"),
    (re.compile(r"\bsolo\s+founder\b", re.I), "CTO"),
    (re.compile(r"\bneed\s+a\s+(serious\s+)?technical\s+co[- ]?founder\b", re.I), "CTO"),
    (re.compile(r"\bmobile\s+money\b", re.I), "Operations Lead"),
    (re.compile(r"\b(need|looking for|require|hiring|book(ing)?)\s+(\d+\s+)?violin(ist)?s?\b", re.I), "Violinist"),
    (re.compile(r"\bneed\s+(an?\s+)?(audio|sound|mixing|mastering)\s+engineer\b", re.I), "Audio Engineer"),
    (re.compile(r"\bneed\s+(an?\s+)?(composer|arranger)\b", re.I), "Composer"),
]

_STAGE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b(launched|live|in production|paying customers|revenue)\b", re.I), "launched"),
    (re.compile(r"\b(prototype|mvp|beta|pilot|alpha)\b", re.I), "prototype"),
]


def _detect_category(text: str) -> str:
    t = text.lower()
    for cat, kws in _CATEGORY_KEYWORDS:
        if any(kw in t for kw in kws):
            return cat
    return "b2b saas"


def _detect_stage(text: str) -> str:
    for pat, stage in _STAGE_PATTERNS:
        if pat.search(text):
            return stage
    return "idea"


def _detect_missing_roles(text: str, category: str) -> list[str]:
    found: list[str] = []
    for pat, role in _LACK_PATTERNS:
        if pat.search(text) and role not in found:
            found.append(role)
    if not found:
        # No explicit signal — fall back to the canonical first role for the category.
        found = _CATEGORY_ROLES[category][:2]
    return found[:4]


def _extract_one_liner(text: str) -> str:
    # First sentence, trimmed to ~18 words.
    first = re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=1)[0]
    words = first.split()
    if len(words) > 18:
        first = " ".join(words[:18]) + "…"
    return first.rstrip(".") + "."


def _extract_problem(text: str) -> str:
    # Use the first 1-2 sentences as the problem statement.
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(parts[:2]).strip()


def _extract_target_user(text: str) -> str:
    t = text.lower()
    candidates = [
        ("medical students", ["med student", "medical student"]),
        ("small and mid-sized businesses", ["smb", "small and mid", "small business"]),
        ("lawyers and legal teams", ["lawyer", "legal team"]),
        ("informal retailers in West Africa", ["informal retail", "west africa", "kiosk"]),
        ("film and festival audiences", ["film score", "festival", "film composer"]),
        ("listeners of orchestral music", ["orchestral", "symphony", "string quartet", "ensemble"]),
        ("developers", ["developer", "engineer"]),
        ("founders", ["founder"]),
        ("clinicians", ["doctor", "clinician", "physician"]),
    ]
    for label, kws in candidates:
        if any(kw in t for kw in kws):
            return label
    return "early-stage operators"


def _structure_via_mock(raw: str) -> dict:
    category = _detect_category(raw)
    stage = _detect_stage(raw)
    missing = _detect_missing_roles(raw, category)
    skills = _CATEGORY_SKILLS[category][:5]
    advice = _build_advice(raw, category)

    return _normalize({
        "one_liner": _extract_one_liner(raw),
        "problem": _extract_problem(raw),
        "target_user": _extract_target_user(raw),
        "category": category,
        "stage": stage,
        "required_skills": skills,
        "missing_roles": missing,
        "advice": advice,
    }, raw)


def _build_advice(text: str, category: str) -> list[str]:
    """Pick 3 category-appropriate tweaks, with light contextual swap-ins."""
    advice = list(_CATEGORY_ADVICE.get(category, _CATEGORY_ADVICE["b2b saas"]))

    # Light context: if the founder mentions an explicit duration for a music
    # piece, personalise the duration tip with their actual number.
    if category == "music":
        m = re.search(r"\b(\d{1,2})[- ]?minute(s)?\b", text, re.I)
        if m:
            mins = int(m.group(1))
            if mins >= 9:
                target = max(6, mins - 4)
                advice[0] = (
                    f"Trim the piece from {mins} to ~{target} minutes — most festival "
                    "shortlists cap entries around 10."
                )
    return advice[:3]


# ---------- Normalization ----------

def _normalize(d: dict, raw: str) -> dict:
    """Defensive: enforce the schema regardless of source quirks."""
    cat = str(d.get("category", "b2b saas")).lower().strip()
    if cat not in CATEGORIES:
        cat = "b2b saas"
    stage = str(d.get("stage", "idea")).lower().strip()
    if stage not in STAGES:
        stage = "idea"

    def _str_list(v, default):
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()][:7] or default
        return default

    return {
        "one_liner": str(d.get("one_liner") or _extract_one_liner(raw))[:180],
        "problem": str(d.get("problem") or _extract_problem(raw))[:480],
        "target_user": str(d.get("target_user") or "early-stage operators")[:120],
        "category": cat,
        "stage": stage,
        "required_skills": _str_list(d.get("required_skills"), _CATEGORY_SKILLS[cat][:5]),
        "missing_roles": _str_list(d.get("missing_roles"), _CATEGORY_ROLES[cat][:2])[:4],
        "advice": _str_list(d.get("advice"), _CATEGORY_ADVICE.get(cat, _CATEGORY_ADVICE["b2b saas"])[:3])[:4],
    }
