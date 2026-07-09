"""
analysis/confluence.py
Aggregate confluence score wrapper kept separate from scoring.py so the
decision engine can call a single stable entrypoint even if scoring logic
changes internally.
"""
from analysis.scoring import compute_confluence_score


def get_confluence(df, indicators: dict) -> dict:
    return compute_confluence_score(df, indicators)
