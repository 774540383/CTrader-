"""
ai/memory.py
Lightweight rolling memory of recent AI decisions, used to give the model
context about its own recent behaviour and avoid repeated mistakes.
"""
from collections import deque

_MAX_HISTORY = 20
_history = deque(maxlen=_MAX_HISTORY)


def record_decision(market_data: dict, decision: dict):
    _history.append({
        "symbol": market_data.get("symbol"),
        "decision": decision.get("decision"),
        "confidence": decision.get("confidence"),
    })


def get_recent_history() -> list:
    return list(_history)


def summarize_recent() -> str:
    if not _history:
        return "No prior decisions."
    lines = [f"{h['decision']} (conf={h['confidence']})" for h in _history]
    return "; ".join(lines)
