"""Mock founder pool, sample ideas, and the 'current founder' for the Trust Dashboard."""
from __future__ import annotations

SAMPLE_IDEAS: list[dict] = [
    {
        "title": "AI tutor for med students",
        "text": (
            "An AI tutor that helps medical students study for board exams by generating "
            "personalized clinical case simulations from their weakest topic areas. It "
            "watches how they reason through cases and adapts difficulty in real time. "
            "Right now I'm a solo founder, technical-ish, but I have no clinical background "
            "and no design help."
        ),
    },
    {
        "title": "Carbon credits for SMBs",
        "text": (
            "A marketplace where small and mid-sized businesses can buy verified carbon "
            "credits as easily as buying a Stripe subscription — bundle the accounting, "
            "the certificate, and the regulatory paperwork into a single SaaS product. "
            "Targeting EU SMBs hit by CSRD reporting. I'm a climate-finance person, not "
            "a builder."
        ),
    },
    {
        "title": "Figma for legal contracts",
        "text": (
            "A collaborative editor for legal contracts where lawyers, founders, and "
            "counterparties can redline together in real time, with an AI layer that "
            "explains every clause in plain English and flags risk. Think Figma + "
            "Notion for law. I'm a lawyer turned PM, no engineering."
        ),
    },
    {
        "title": "Offline-first POS for African retail",
        "text": (
            "An offline-first point-of-sale and inventory system for informal retailers "
            "across West Africa — runs on cheap Android phones, syncs when there's "
            "signal, and gives shop owners credit scoring based on real sales data. "
            "I'm a Nigerian operator who has run kiosks. I need a serious technical "
            "co-founder and someone who knows mobile money rails."
        ),
    },
    {
        "title": "Orchestral track for a film score",
        "text": (
            "I'm a producer finishing an orchestral piece for an indie film score — a "
            "12-minute arrangement that opens with a solo violin and builds into a full "
            "string section. I need 8 violinists who can handle contemporary classical "
            "notation and are comfortable in a one-day studio session. I'm based in Paris "
            "and targeting the Cannes short film festival window. I'll handle the "
            "arrangement and production myself but need help scouting players."
        ),
    },
]


# Twelve hand-crafted founder profiles. Roles, skills, and category history are
# designed to give the matching engine real signal — there should be obvious
# matches and obvious non-matches per sample idea.
MOCK_USERS: list[dict] = [
    {
        "name": "Maya Okafor",
        "headline": "Ex-Stripe infra eng — built payments for 3 fintechs",
        "role": "CTO",
        "skills": ["Python", "Distributed Systems", "Payments", "Postgres", "AWS"],
        "categories": ["fintech", "b2b saas"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 7,
        "milestones_shipped": 22,
        "endorsements": 14,
        "on_time_rate": 0.92,
        "avatar_color": "#7C5CFF",
        "initials": "MO",
        "recent_projects": [
            {"name": "Ledgerly", "year": 2024, "collaborators": ["A. Park", "J. Tan"]},
            {"name": "Tabby Pay", "year": 2023, "collaborators": ["R. Vasquez"]},
        ],
    },
    {
        "name": "Daniel Park",
        "headline": "Product designer, 2× YC, design systems nerd",
        "role": "Designer",
        "skills": ["Figma", "Design Systems", "Brand", "User Research", "Prototyping"],
        "categories": ["consumer", "devtools", "b2b saas"],
        "stages_shipped": ["idea", "prototype", "launched"],
        "collaborations": 9,
        "milestones_shipped": 31,
        "endorsements": 22,
        "on_time_rate": 0.95,
        "avatar_color": "#3DD8E8",
        "initials": "DP",
        "recent_projects": [
            {"name": "Notch", "year": 2024, "collaborators": ["M. Okafor"]},
            {"name": "Lumen Docs", "year": 2023, "collaborators": ["S. Hadid", "K. Wu"]},
        ],
    },
    {
        "name": "Dr. Aisha Rahman",
        "headline": "MD, internal medicine — 6 yrs clinical, EMR product advisor",
        "role": "Clinical Lead",
        "skills": ["Clinical Workflows", "Medical Education", "HIPAA", "EMR", "Content"],
        "categories": ["healthtech"],
        "stages_shipped": ["prototype"],
        "collaborations": 3,
        "milestones_shipped": 8,
        "endorsements": 11,
        "on_time_rate": 0.88,
        "avatar_color": "#F472B6",
        "initials": "AR",
        "recent_projects": [
            {"name": "RoundsAI", "year": 2024, "collaborators": ["L. Ito"]},
        ],
    },
    {
        "name": "Léo Martin",
        "headline": "ML engineer — RAG, eval, fine-tuning at production scale",
        "role": "ML Engineer",
        "skills": ["Python", "PyTorch", "LLMs", "RAG", "Evals", "Vector DBs"],
        "categories": ["devtools", "healthtech", "b2b saas"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 5,
        "milestones_shipped": 17,
        "endorsements": 9,
        "on_time_rate": 0.90,
        "avatar_color": "#A78BFA",
        "initials": "LM",
        "recent_projects": [
            {"name": "Evalkit", "year": 2024, "collaborators": ["D. Park"]},
        ],
    },
    {
        "name": "Sara Hadid",
        "headline": "GTM lead — took 2 SaaS from $0 to $2M ARR",
        "role": "GTM Lead",
        "skills": ["Sales", "Pricing", "Outbound", "Lifecycle", "Partnerships"],
        "categories": ["b2b saas", "fintech", "climate"],
        "stages_shipped": ["launched"],
        "collaborations": 6,
        "milestones_shipped": 19,
        "endorsements": 13,
        "on_time_rate": 0.87,
        "avatar_color": "#34D399",
        "initials": "SH",
        "recent_projects": [
            {"name": "Lumen Docs", "year": 2023, "collaborators": ["D. Park"]},
            {"name": "Greenstack", "year": 2024, "collaborators": ["R. Vasquez"]},
        ],
    },
    {
        "name": "Rafael Vasquez",
        "headline": "Climate-finance operator, ex-South Pole, CSRD specialist",
        "role": "Domain Expert",
        "skills": ["Carbon Markets", "CSRD", "ESG Reporting", "Verification", "Policy"],
        "categories": ["climate", "fintech"],
        "stages_shipped": ["idea", "launched"],
        "collaborations": 4,
        "milestones_shipped": 11,
        "endorsements": 8,
        "on_time_rate": 0.83,
        "avatar_color": "#22C55E",
        "initials": "RV",
        "recent_projects": [
            {"name": "Greenstack", "year": 2024, "collaborators": ["S. Hadid"]},
        ],
    },
    {
        "name": "Kenji Wu",
        "headline": "Mobile engineer — offline-first apps, 50M+ installs",
        "role": "Mobile Engineer",
        "skills": ["Kotlin", "Android", "Offline Sync", "SQLite", "React Native"],
        "categories": ["consumer", "fintech"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 5,
        "milestones_shipped": 16,
        "endorsements": 10,
        "on_time_rate": 0.91,
        "avatar_color": "#60A5FA",
        "initials": "KW",
        "recent_projects": [
            {"name": "Lumen Docs", "year": 2023, "collaborators": ["D. Park", "S. Hadid"]},
            {"name": "Pesa Lite", "year": 2024, "collaborators": ["O. Adeyemi"]},
        ],
    },
    {
        "name": "Olamide Adeyemi",
        "headline": "Lagos-based ops lead, mobile money + agent networks",
        "role": "Operations Lead",
        "skills": ["Mobile Money", "Agent Networks", "Compliance", "Field Ops", "West Africa"],
        "categories": ["fintech", "consumer"],
        "stages_shipped": ["launched"],
        "collaborations": 4,
        "milestones_shipped": 14,
        "endorsements": 12,
        "on_time_rate": 0.94,
        "avatar_color": "#FB923C",
        "initials": "OA",
        "recent_projects": [
            {"name": "Pesa Lite", "year": 2024, "collaborators": ["K. Wu"]},
        ],
    },
    {
        "name": "Jules Tan",
        "headline": "Backend engineer — Go, Postgres, observability obsessive",
        "role": "Backend Engineer",
        "skills": ["Go", "Postgres", "Kubernetes", "Observability", "APIs"],
        "categories": ["devtools", "b2b saas"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 3,
        "milestones_shipped": 12,
        "endorsements": 6,
        "on_time_rate": 0.89,
        "avatar_color": "#38BDF8",
        "initials": "JT",
        "recent_projects": [
            {"name": "Ledgerly", "year": 2024, "collaborators": ["M. Okafor"]},
        ],
    },
    {
        "name": "Priya Iyer",
        "headline": "Product lead — legal-tech, ex-Ironclad, ex-DocuSign",
        "role": "Product Lead",
        "skills": ["Legaltech", "Contracts", "Workflow Design", "Discovery", "PRDs"],
        "categories": ["b2b saas", "legaltech"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 5,
        "milestones_shipped": 18,
        "endorsements": 11,
        "on_time_rate": 0.86,
        "avatar_color": "#F59E0B",
        "initials": "PI",
        "recent_projects": [
            {"name": "ClauseLab", "year": 2023, "collaborators": ["E. Bauer"]},
        ],
    },
    {
        "name": "Elena Bauer",
        "headline": "Full-stack engineer, real-time collab (CRDTs, OT, Y.js)",
        "role": "Full-Stack Engineer",
        "skills": ["TypeScript", "React", "CRDTs", "WebSockets", "Postgres"],
        "categories": ["b2b saas", "devtools", "legaltech"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 6,
        "milestones_shipped": 20,
        "endorsements": 9,
        "on_time_rate": 0.93,
        "avatar_color": "#C084FC",
        "initials": "EB",
        "recent_projects": [
            {"name": "ClauseLab", "year": 2023, "collaborators": ["P. Iyer"]},
            {"name": "Notch", "year": 2024, "collaborators": ["D. Park"]},
        ],
    },
    {
        "name": "Camille Fournier",
        "headline": "Conservatoire de Paris grad — session violinist, 40+ film scores",
        "role": "Violinist",
        "skills": ["Violin", "Studio Recording", "Sight Reading", "Contemporary Classical", "Film Scoring"],
        "categories": ["music"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 6,
        "milestones_shipped": 18,
        "endorsements": 12,
        "on_time_rate": 0.96,
        "avatar_color": "#E879F9",
        "initials": "CF",
        "recent_projects": [
            {"name": "Lumière (short film)", "year": 2024, "collaborators": ["N. Laurent"]},
        ],
    },
    {
        "name": "Noah Laurent",
        "headline": "Freelance violinist — chamber + session, Paris-based",
        "role": "Violinist",
        "skills": ["Violin", "Sight Reading", "Chamber Music", "Studio Recording", "Arrangement"],
        "categories": ["music"],
        "stages_shipped": ["prototype", "launched"],
        "collaborations": 4,
        "milestones_shipped": 13,
        "endorsements": 8,
        "on_time_rate": 0.92,
        "avatar_color": "#F0ABFC",
        "initials": "NL",
        "recent_projects": [
            {"name": "Lumière (short film)", "year": 2024, "collaborators": ["C. Fournier"]},
        ],
    },
    {
        "name": "Ines Costa",
        "headline": "Violinist + string contractor — books Paris session ensembles",
        "role": "Violinist",
        "skills": ["Violin", "Session Contracting", "Music Theory", "Studio Recording", "Sight Reading"],
        "categories": ["music"],
        "stages_shipped": ["launched"],
        "collaborations": 7,
        "milestones_shipped": 21,
        "endorsements": 14,
        "on_time_rate": 0.94,
        "avatar_color": "#D946EF",
        "initials": "IC",
        "recent_projects": [
            {"name": "Nocturne EP", "year": 2024, "collaborators": ["C. Fournier"]},
        ],
    },
    {
        "name": "Liam Ito",
        "headline": "Learning-science researcher — adaptive assessment, EdTech R&D",
        "role": "Learning Scientist",
        "skills": ["Adaptive Learning", "Psychometrics", "Curriculum", "Evals", "Content"],
        "categories": ["healthtech", "consumer", "edtech"],
        "stages_shipped": ["idea", "prototype"],
        "collaborations": 3,
        "milestones_shipped": 9,
        "endorsements": 7,
        "on_time_rate": 0.85,
        "avatar_color": "#F472B6",
        "initials": "LI",
        "recent_projects": [
            {"name": "RoundsAI", "year": 2024, "collaborators": ["A. Rahman"]},
        ],
    },
]


# The "you" profile shown in the Trust Dashboard. Numbers are deliberately
# strong-but-believable so the dashboard reads as a credible founder.
CURRENT_FOUNDER: dict = {
    "name": "You",
    "headline": "Building Dvoider — execution-based social proof for founders",
    "role": "Founder",
    "collaborations": 8,
    "milestones_shipped": 27,
    "endorsements": 16,
    "on_time_rate": 0.91,
    "avatar_color": "#7C5CFF",
    "initials": "YO",
    "milestones_by_quarter": [
        ("Q2 '24", 3),
        ("Q3 '24", 5),
        ("Q4 '24", 6),
        ("Q1 '25", 4),
        ("Q2 '25", 5),
        ("Q3 '25", 4),
    ],
    "execution_receipts": [
        {"name": "Ledgerly v1 launch", "date": "Mar 2024", "collaborators": ["Maya Okafor", "Jules Tan"]},
        {"name": "Notch design system", "date": "Jul 2024", "collaborators": ["Daniel Park", "Elena Bauer"]},
        {"name": "Greenstack pilot", "date": "Nov 2024", "collaborators": ["Rafael Vasquez", "Sara Hadid"]},
        {"name": "Pesa Lite v0", "date": "Feb 2025", "collaborators": ["Kenji Wu", "Olamide Adeyemi"]},
    ],
}
