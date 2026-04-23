# Dvoider — investor MVP demo

An execution engine for early founders: paste a raw startup idea, watch the AI structure it into a Project Profile, get the top 3 co-founder matches from a mock founder pool, and inspect the Trust Dashboard that proves real shipped work.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The demo runs **fully offline** by default using a deterministic mock for the AI step.

To switch to live GPT-4o-mini, either:

```bash
export OPENAI_API_KEY=sk-...
streamlit run app.py
```

…or paste a key into the sidebar field at runtime. Live calls fall back to the mock if anything fails — the pitch never breaks.

## Demo flow

1. **The Lab** — pick a sample idea from the sidebar (or paste your own) and click *Structure with AI*.
2. **The Architect** — Dvoider extracts problem, category, stage, required skills, and missing roles into a single Project Profile card.
3. **The Matchmaker** — top 3 co-founders ranked by role fit + skill complementarity + category track-record, each with a "why this match" rationale.
4. **The Trust Dashboard** — execution-based social proof: milestones, on-time rate, and verifiable shipped projects.

## Files

- `app.py` — Streamlit entrypoint and 4-step flow
- `ai.py` — `structure_idea()` with OpenAI + mock backends
- `matching.py` — pure scoring functions for the matchmaker
- `mock_data.py` — founder pool, sample ideas, current-founder profile
- `styles.py` — dark premium CSS theme
