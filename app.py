"""Dvoider — MVP demo (Streamlit)."""
from __future__ import annotations

import html
import os
import time

import pandas as pd
import streamlit as st

from ai import structure_idea
from matching import rank_cofounders
from mock_data import CURRENT_FOUNDER, MOCK_USERS, SAMPLE_IDEAS
from styles import inject_css

# ---------- Page setup ----------

st.set_page_config(
    page_title="Dvoider — Idea to Team",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()


# ---------- Session state ----------

def _init_state() -> None:
    defaults = {
        "step": 1,                 # 1..4 — the highest revealed step
        "raw_idea": "",
        "profile": None,           # dict
        "matches": None,           # list
        "source": None,            # 'live' | 'mock' | 'mock-fallback'
        "api_key": "",
        "prefill_idx": None,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


_init_state()


def _reset() -> None:
    for k in ("step", "raw_idea", "profile", "matches", "source", "prefill_idx"):
        st.session_state.pop(k, None)
    _init_state()


# ---------- Small render helpers ----------

def _pill(text: str, variant: str = "") -> str:
    cls = "dv-pill" + (f" {variant}" if variant else "")
    return f'<span class="{cls}">{html.escape(text)}</span>'


def _avatar(initials: str, color: str, size: int = 44) -> str:
    return (
        f'<div class="dv-avatar" style="background:{color}; width:{size}px; height:{size}px;">'
        f"{html.escape(initials)}</div>"
    )


def _step_label(num: int, label: str) -> None:
    st.markdown(
        f'<div class="dv-step"><span class="num">{num}</span>{html.escape(label)}</div>',
        unsafe_allow_html=True,
    )


# ---------- Sidebar ----------

with st.sidebar:
    st.markdown(
        '<div class="dv-wordmark">Dvoider<span class="dot">.</span></div>'
        '<div class="dv-muted" style="font-size:0.85rem; margin-bottom:1.6rem;">'
        "Turn ideas into teams.</div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="dv-muted" style="font-size:0.72rem; letter-spacing:0.16em; '
                'text-transform:uppercase; margin-bottom:6px;">AI backend</div>',
                unsafe_allow_html=True)

    api_key_input = st.text_input(
        "OpenAI API key (optional)",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-…  leave blank to run on the mock",
        label_visibility="collapsed",
    )
    st.session_state.api_key = api_key_input

    has_key = bool(api_key_input or os.environ.get("OPENAI_API_KEY"))
    badge_html = (
        '<span class="dv-badge live">● Live · gpt-4o-mini</span>' if has_key
        else '<span class="dv-badge mock">○ Mock mode</span>'
    )
    st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown('<div style="height:1.4rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="dv-muted" style="font-size:0.72rem; letter-spacing:0.16em; '
                'text-transform:uppercase; margin-bottom:6px;">Sample ideas</div>',
                unsafe_allow_html=True)

    for i, sample in enumerate(SAMPLE_IDEAS):
        if st.button(sample["title"], key=f"sample-{i}", use_container_width=True):
            st.session_state.raw_idea = sample["text"]
            st.session_state.idea_input = sample["text"]
            st.session_state.prefill_idx = i
            # If user loads a new sample, re-collapse downstream steps.
            st.session_state.step = 1
            st.session_state.profile = None
            st.session_state.matches = None
            st.rerun()

    st.markdown('<div style="height:1.4rem;"></div>', unsafe_allow_html=True)
    if st.button("↺  Reset demo", key="reset", use_container_width=True):
        _reset()
        st.rerun()

    st.markdown(
        '<div class="dv-muted" style="font-size:0.72rem; margin-top:auto; padding-top:2rem;">'
        "v0.1 · preview</div>",
        unsafe_allow_html=True,
    )


# ---------- Hero ----------

st.markdown(
    '<div class="dv-hero">From raw idea to a <span class="grad">founding team</span>.</div>'
    '<div class="dv-tagline">Dvoider is the execution engine for early founders — '
    "structure the idea, find the people, prove the work.</div>",
    unsafe_allow_html=True,
)


# =====================================================================
# STEP 1 — The Lab
# =====================================================================
_step_label(1, "The Lab · drop your raw idea")

idea_text = st.text_area(
    "Idea",
    value=st.session_state.raw_idea,
    height=200,
    placeholder="A short description of what you want to build, who it's for, "
                "and what you're missing as a founder. Messy is fine — that's the point.",
    label_visibility="collapsed",
    key="idea_input",
)

with st.expander("Try a sample idea", expanded=False):
    for i, sample in enumerate(SAMPLE_IDEAS):
        if st.button(sample["title"], key=f"main-sample-{i}", use_container_width=True):
            st.session_state.raw_idea = sample["text"]
            st.session_state.idea_input = sample["text"]
            st.session_state.prefill_idx = i
            st.session_state.step = 1
            st.session_state.profile = None
            st.session_state.matches = None
            st.rerun()

c1, c2 = st.columns([1, 5])
with c1:
    structure_clicked = st.button("Structure with AI →", type="primary", use_container_width=True)
with c2:
    if st.session_state.prefill_idx is not None:
        st.markdown(
            f'<div class="dv-muted" style="padding-top:0.55rem;">Loaded sample · '
            f'<b>{html.escape(SAMPLE_IDEAS[st.session_state.prefill_idx]["title"])}</b></div>',
            unsafe_allow_html=True,
        )

if structure_clicked:
    if not idea_text.strip():
        st.warning("Paste an idea first — even a rough one.")
    else:
        st.session_state.raw_idea = idea_text
        with st.status("Architecting your idea…", expanded=True) as status:
            st.write("→ Extracting the underlying problem")
            time.sleep(0.5)
            st.write("→ Identifying category and stage")
            time.sleep(0.45)
            st.write("→ Mapping required skills")
            time.sleep(0.45)
            st.write("→ Detecting missing roles")
            time.sleep(0.4)
            try:
                profile, source = structure_idea(idea_text, st.session_state.api_key or None)
            except Exception as e:
                status.update(label=f"Failed: {e}", state="error")
                st.stop()
            st.session_state.profile = profile
            st.session_state.source = source
            st.session_state.matches = rank_cofounders(profile, MOCK_USERS, top_n=3)
            st.session_state.step = max(st.session_state.step, 3)
            status.update(label="Architected ✓", state="complete", expanded=False)
        if source == "mock-fallback":
            st.toast("Live API unavailable — falling back to the mock.", icon="⚠️")
        st.rerun()


# =====================================================================
# STEP 2 — The Architect (Project Profile card)
# =====================================================================
if st.session_state.profile:
    st.markdown('<div class="dv-divider"></div>', unsafe_allow_html=True)
    src = st.session_state.source
    src_badge = (
        '<span class="dv-badge live">● Live</span>' if src == "live"
        else '<span class="dv-badge mock">○ Mock</span>'
    )
    _step_label(2, "The Architect · structured Project Profile")

    p = st.session_state.profile
    skills_html = "".join(_pill(s) for s in p["required_skills"])
    roles_html = "".join(_pill(r, "warn") for r in p["missing_roles"])
    cat_pill = _pill(p["category"], "cyan")
    stage_pill = _pill(p["stage"].capitalize(), "muted")
    advice_items = p.get("advice") or []
    advice_html = "".join(
        f'<li style="margin-bottom:0.45rem; line-height:1.45;">{html.escape(a)}</li>'
        for a in advice_items
    )

    st.markdown(
        f"""
        <div class="dv-card">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem;">
            <div>
              <h4>One-liner</h4>
              <div style="font-size:1.25rem; font-weight:600; line-height:1.3;">
                {html.escape(p['one_liner'])}
              </div>
            </div>
            <div>{src_badge}</div>
          </div>
          <div style="height:1.1rem;"></div>
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 1.6rem;">
            <div>
              <h4>Problem</h4>
              <div class="dv-quote">{html.escape(p['problem'])}</div>
              <div style="height:0.9rem;"></div>
              <h4>Target user</h4>
              <div>{html.escape(p['target_user'])}</div>
            </div>
            <div>
              <h4>Category &amp; stage</h4>
              <div>{cat_pill}{stage_pill}</div>
              <div style="height:0.9rem;"></div>
              <h4>Required skills</h4>
              <div>{skills_html}</div>
              <div style="height:0.9rem;"></div>
              <h4>Missing roles</h4>
              <div>{roles_html}</div>
            </div>
          </div>
          {'<div style="height:1.1rem;"></div><h4>Suggested tweaks</h4><ul class="dv-advice">' + advice_html + '</ul>' if advice_html else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =====================================================================
# STEP 3 — The Matchmaker
# =====================================================================
if st.session_state.matches:
    st.markdown('<div class="dv-divider"></div>', unsafe_allow_html=True)
    _step_label(3, "The Matchmaker · top co-founders for this profile")
    st.markdown(
        '<div class="dv-tagline" style="margin-top:-0.4rem;">'
        "Ranked by role fit, skill complementarity, and category track-record across "
        f"{len(MOCK_USERS)} founders in the Dvoider pool.</div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="medium")
    for col, m in zip(cols, st.session_state.matches):
        breakdown = m["score_breakdown"]
        overlap_chips = "".join(_pill(s, "cyan") for s in m["skill_overlap"][:3]) or \
            '<span class="dv-muted" style="font-size:0.8rem;">No direct skill overlap</span>'
        with col:
            st.markdown(
                f"""
                <div class="dv-match">
                  <div style="display:flex; gap:0.8rem; align-items:center;">
                    {_avatar(m['initials'], m['avatar_color'])}
                    <div style="min-width:0;">
                      <div class="name">{html.escape(m['name'])}</div>
                      <div class="headline">{html.escape(m['headline'])}</div>
                    </div>
                  </div>
                  <div style="height:0.9rem;"></div>
                  <div style="display:flex; align-items:baseline; gap:0.6rem;">
                    <div class="score">{m['score']}</div>
                    <div class="score-label">Match score</div>
                  </div>
                  <div class="breakdown">
                    Role fit {breakdown['role_fit']} · Skills {breakdown['skill_complementarity']} ·
                    Affinity {breakdown['stage_category_affinity']} ·
                    Reliability {breakdown['reliability']}
                  </div>
                  <div style="height:0.8rem;"></div>
                  <div class="dv-muted" style="font-size:0.72rem; letter-spacing:0.14em;
                       text-transform:uppercase; margin-bottom:6px;">Skill overlap</div>
                  <div>{overlap_chips}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("Why this match", expanded=False):
                st.write(m["rationale"])
                st.markdown(
                    f"<div class='dv-muted' style='font-size:0.82rem;'>"
                    f"{m['milestones_shipped']} milestones shipped · "
                    f"{m['collaborations']} collaborations · "
                    f"{int(m['on_time_rate']*100)}% on-time</div>",
                    unsafe_allow_html=True,
                )
            st.button("Request intro", key=f"intro-{m['name']}", use_container_width=True)

    st.markdown('<div style="height:0.6rem;"></div>', unsafe_allow_html=True)
    if st.button("See the founder's Trust Dashboard →", type="primary"):
        st.session_state.step = 4
        st.rerun()


# =====================================================================
# STEP 4 — The Trust Dashboard
# =====================================================================
if st.session_state.step >= 4:
    st.markdown('<div class="dv-divider"></div>', unsafe_allow_html=True)
    _step_label(4, "The Trust Dashboard · execution-based social proof")
    st.markdown(
        '<div class="dv-tagline" style="margin-top:-0.4rem;">'
        "Every founder on Dvoider has a public ledger of what they've actually shipped — "
        "not endorsements you can buy, but receipts you can verify.</div>",
        unsafe_allow_html=True,
    )

    f = CURRENT_FOUNDER
    h1, h2 = st.columns([1, 6])
    with h1:
        st.markdown(_avatar(f["initials"], f["avatar_color"], size=72), unsafe_allow_html=True)
    with h2:
        st.markdown(
            f"<div style='font-size:1.4rem; font-weight:650;'>{html.escape(f['name'])}</div>"
            f"<div class='dv-muted'>{html.escape(f['headline'])}</div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Collaborations", f["collaborations"])
    m2.metric("Milestones shipped", f["milestones_shipped"])
    m3.metric("On-time rate", f"{int(f['on_time_rate']*100)}%")
    m4.metric("Endorsements", f["endorsements"])

    st.markdown('<div style="height:1.2rem;"></div>', unsafe_allow_html=True)
    cc1, cc2 = st.columns([3, 2], gap="large")
    with cc1:
        st.markdown(
            '<div class="dv-muted" style="font-size:0.72rem; letter-spacing:0.14em; '
            'text-transform:uppercase; margin-bottom:6px;">Milestones shipped per quarter</div>',
            unsafe_allow_html=True,
        )
        df = pd.DataFrame(f["milestones_by_quarter"], columns=["Quarter", "Milestones"]).set_index("Quarter")
        st.bar_chart(df, height=240, color="#7C5CFF")
    with cc2:
        st.markdown(
            '<div class="dv-muted" style="font-size:0.72rem; letter-spacing:0.14em; '
            'text-transform:uppercase; margin-bottom:6px;">Execution receipts</div>',
            unsafe_allow_html=True,
        )
        for r in f["execution_receipts"]:
            collabs = " · ".join(r["collaborators"])
            st.markdown(
                f"""
                <div class="dv-receipt">
                  <div>
                    <div style="font-weight:600;">{html.escape(r['name'])}</div>
                    <div class="meta">with {html.escape(collabs)}</div>
                  </div>
                  <div class="meta">{html.escape(r['date'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------- Footer ----------

st.markdown(
    '<div class="dv-footer">Dvoider — execution-based social proof for founders.</div>',
    unsafe_allow_html=True,
)
