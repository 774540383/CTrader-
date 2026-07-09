"""
execution/strategy.py
High-level strategy wrapper: decides HOW to enter (market order now vs
waiting for confirmation) based on the AI decision and confluence score.
"""


def choose_entry_strategy(decision: dict, confluence: dict) -> str:
    score = confluence.get("confluence_score", 0)
    confidence = decision.get("confidence", 0)

    if confidence >= 90 and abs(score) >= 40:
        return "MARKET_ORDER"
    if confidence >= 85:
        return "LIMIT_ORDER"
    return "NO_ENTRY"
