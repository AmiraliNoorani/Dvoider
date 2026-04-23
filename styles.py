"""Dvoider visual theme — dark premium, Linear/Vercel-ish aesthetic."""
import streamlit as st

BG = "#0B0B0F"
SURFACE = "#15151C"
SURFACE_2 = "#1B1B24"
BORDER = "#26262F"
TEXT = "#EDEDF2"
MUTED = "#8A8A99"
ACCENT = "#7C5CFF"
ACCENT_2 = "#3DD8E8"
SUCCESS = "#4ADE80"
WARN = "#F59E0B"

CSS = f"""
:root {{
  --dv-bg: {BG};
  --dv-surface: {SURFACE};
  --dv-surface-2: {SURFACE_2};
  --dv-border: {BORDER};
  --dv-text: {TEXT};
  --dv-muted: {MUTED};
  --dv-accent: {ACCENT};
  --dv-accent-2: {ACCENT_2};
}}

html, body, [class*="css"], .stApp {{
  background-color: var(--dv-bg) !important;
  color: var(--dv-text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: -0.005em;
}}

.stApp {{ background: radial-gradient(1200px 600px at 80% -10%, rgba(124,92,255,0.12), transparent 60%),
                       radial-gradient(900px 500px at -10% 10%, rgba(61,216,232,0.07), transparent 60%),
                       var(--dv-bg) !important; }}

section[data-testid="stSidebar"] {{
  background-color: #0E0E14 !important;
  border-right: 1px solid var(--dv-border);
}}
section[data-testid="stSidebar"] * {{ color: var(--dv-text) !important; }}

h1, h2, h3, h4 {{
  color: var(--dv-text) !important;
  letter-spacing: -0.02em;
  font-weight: 650;
}}
h1 {{ font-size: 2.4rem; line-height: 1.1; }}
h2 {{ font-size: 1.6rem; }}
h3 {{ font-size: 1.15rem; color: var(--dv-muted) !important; font-weight: 500; }}

p, li, span, label {{ color: var(--dv-text); }}
small, .dv-muted {{ color: var(--dv-muted) !important; }}

/* Hero */
.dv-hero {{
  font-size: clamp(1.8rem, 6vw, 3.2rem);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.03em;
  margin: 0.4rem 0 0.6rem 0;
}}
.dv-hero .grad {{
  background: linear-gradient(90deg, {ACCENT} 0%, {ACCENT_2} 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.dv-tagline {{
  color: var(--dv-muted);
  font-size: 1.05rem;
  margin-bottom: 1.4rem;
}}

/* Cards */
.dv-card {{
  background: linear-gradient(180deg, var(--dv-surface) 0%, var(--dv-surface-2) 100%);
  border: 1px solid var(--dv-border);
  border-radius: 16px;
  padding: 1.4rem 1.5rem;
  margin: 0.5rem 0 1rem 0;
  box-shadow: 0 1px 0 rgba(255,255,255,0.02) inset, 0 18px 40px -24px rgba(0,0,0,0.6);
}}
.dv-card h4 {{
  color: var(--dv-muted) !important;
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}}
.dv-card .dv-quote {{
  border-left: 2px solid var(--dv-accent);
  padding-left: 0.85rem;
  font-size: 1.05rem;
  color: var(--dv-text);
  margin: 0.2rem 0 0.3rem 0;
}}
.dv-card ul.dv-advice {{
  list-style: none;
  padding: 0;
  margin: 0.2rem 0 0 0;
}}
.dv-card ul.dv-advice li {{
  position: relative;
  padding-left: 1.3rem;
  color: var(--dv-text);
  font-size: 0.95rem;
}}
.dv-card ul.dv-advice li::before {{
  content: "→";
  position: absolute;
  left: 0;
  color: var(--dv-accent-2);
  font-weight: 700;
}}

/* Pills + chips */
.dv-pill {{
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 500;
  background: rgba(124,92,255,0.10);
  color: #C4B6FF;
  border: 1px solid rgba(124,92,255,0.25);
  margin: 2px 4px 2px 0;
}}
.dv-pill.cyan {{
  background: rgba(61,216,232,0.10);
  color: #9DEEF7;
  border-color: rgba(61,216,232,0.25);
}}
.dv-pill.warn {{
  background: rgba(245,158,11,0.10);
  color: #FCD27A;
  border-color: rgba(245,158,11,0.30);
}}
.dv-pill.muted {{
  background: rgba(255,255,255,0.04);
  color: var(--dv-muted);
  border-color: var(--dv-border);
}}

/* Avatar */
.dv-avatar {{
  width: 44px; height: 44px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  color: white; font-weight: 600; font-size: 1rem; letter-spacing: 0.02em;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 6px 18px -6px rgba(0,0,0,0.6);
}}

/* Match card */
.dv-match {{
  background: linear-gradient(180deg, var(--dv-surface) 0%, var(--dv-surface-2) 100%);
  border: 1px solid var(--dv-border);
  border-radius: 16px;
  padding: 1.1rem 1.1rem 1rem;
  height: 100%;
}}
.dv-match .name {{ font-size: 1.05rem; font-weight: 600; margin: 0; }}
.dv-match .headline {{ color: var(--dv-muted); font-size: 0.85rem; margin-top: 2px; }}
.dv-match .score {{
  font-size: 2rem; font-weight: 700; letter-spacing: -0.02em;
  background: linear-gradient(90deg, {ACCENT} 0%, {ACCENT_2} 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.dv-match .score-label {{ color: var(--dv-muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.14em; }}
.dv-match .breakdown {{ font-size: 0.78rem; color: var(--dv-muted); margin-top: 4px; }}

/* Buttons */
.stButton > button {{
  background: var(--dv-accent) !important;
  color: white !important;
  border: 0 !important;
  border-radius: 10px !important;
  padding: 0.55rem 1.1rem !important;
  font-weight: 600 !important;
  letter-spacing: -0.01em;
  transition: transform 0.06s ease, box-shadow 0.2s ease, background 0.2s ease;
  box-shadow: 0 8px 24px -10px rgba(124,92,255,0.6);
}}
.stButton > button:hover {{
  background: #8A6CFF !important;
  transform: translateY(-1px);
}}
.stButton > button:focus {{ box-shadow: 0 0 0 3px rgba(124,92,255,0.35) !important; }}

.stButton.dv-secondary > button,
button[kind="secondary"] {{
  background: transparent !important;
  color: var(--dv-text) !important;
  border: 1px solid var(--dv-border) !important;
  box-shadow: none !important;
}}
button[kind="secondary"]:hover {{ background: rgba(255,255,255,0.04) !important; }}

/* Text area */
.stTextArea textarea {{
  background-color: var(--dv-surface) !important;
  color: var(--dv-text) !important;
  border: 1px solid var(--dv-border) !important;
  border-radius: 12px !important;
  font-size: 0.98rem !important;
  padding: 0.9rem !important;
}}
.stTextArea textarea:focus {{
  border-color: var(--dv-accent) !important;
  box-shadow: 0 0 0 3px rgba(124,92,255,0.2) !important;
}}
.stTextInput input {{
  background-color: var(--dv-surface) !important;
  color: var(--dv-text) !important;
  border: 1px solid var(--dv-border) !important;
  border-radius: 10px !important;
}}

/* Metric */
[data-testid="stMetric"] {{
  background: linear-gradient(180deg, var(--dv-surface) 0%, var(--dv-surface-2) 100%);
  border: 1px solid var(--dv-border);
  border-radius: 14px;
  padding: 0.9rem 1rem;
}}
[data-testid="stMetricValue"] {{ color: var(--dv-text) !important; font-weight: 650; }}
[data-testid="stMetricLabel"] {{ color: var(--dv-muted) !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.12em; }}

/* Status / expander */
[data-testid="stStatusWidget"], details {{
  background: var(--dv-surface) !important;
  border: 1px solid var(--dv-border) !important;
  border-radius: 12px !important;
  color: var(--dv-text) !important;
}}
.streamlit-expanderHeader {{ color: var(--dv-text) !important; }}

/* Step badge */
.dv-step {{
  display: inline-flex; align-items: center; gap: 8px;
  font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase;
  color: var(--dv-muted); font-weight: 600; margin-bottom: 0.3rem;
}}
.dv-step .num {{
  display: inline-flex; align-items: center; justify-content: center;
  width: 22px; height: 22px; border-radius: 6px;
  background: rgba(124,92,255,0.15); color: #C4B6FF;
  border: 1px solid rgba(124,92,255,0.3);
  font-size: 0.72rem;
}}

/* Divider */
.dv-divider {{ height: 1px; background: var(--dv-border); margin: 2.2rem 0 1.6rem 0; }}

/* Sidebar wordmark */
.dv-wordmark {{ font-size: 1.45rem; font-weight: 700; letter-spacing: -0.02em; margin-bottom: 2px; }}
.dv-wordmark .dot {{ color: var(--dv-accent); }}

/* Mode badges */
.dv-badge {{
  display: inline-block; padding: 3px 9px; border-radius: 999px;
  font-size: 0.7rem; font-weight: 600; letter-spacing: 0.04em;
}}
.dv-badge.live {{ background: rgba(74,222,128,0.12); color: {SUCCESS}; border: 1px solid rgba(74,222,128,0.3); }}
.dv-badge.mock {{ background: rgba(255,255,255,0.06); color: var(--dv-muted); border: 1px solid var(--dv-border); }}

/* Receipts */
.dv-receipt {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.6rem 0.8rem; border: 1px solid var(--dv-border);
  border-radius: 10px; margin-bottom: 6px; background: var(--dv-surface);
}}
.dv-receipt .meta {{ color: var(--dv-muted); font-size: 0.8rem; }}

/* Hide default chrome */
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
.block-container {{ padding-top: 2rem !important; padding-bottom: 4rem !important; max-width: 1180px; }}

/* Footer */
.dv-footer {{ text-align: center; color: var(--dv-muted); font-size: 0.8rem; margin-top: 3rem; }}
"""


def inject_css() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
