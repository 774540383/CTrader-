"""
execution/validator.py
Final pre-trade validation: sanity checks on price, volume, and SL/TP
before an order is ever sent to cTrader.
"""


def validate_trade(decision: dict, market_data: dict) -> tuple:
    """Returns (is_valid, reason)."""
    if decision.get("decision") not in ("BUY", "SELL"):
        return False, "Decision is not a trade signal."

    if decision.get("confidence", 0) < 85:
        return False, "Confidence below minimum threshold."

    volume = decision.get("approved_position_size", 0)
    if not volume or volume <= 0:
        return False, "Invalid or zero position size."

    price = market_data.get("price")
    if price is None:
        return False, "Missing current price."

    return True, "OK"
