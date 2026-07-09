"""
risk/trailing_stop.py
Trailing stop calculation logic for open positions.
"""


def calculate_trailing_stop(entry_price: float, current_price: float, side: str,
                             trail_distance: float) -> float:
    """Return the new stop-loss price for a trailing stop, or None if not yet in profit."""
    if side.upper() == "BUY":
        candidate = current_price - trail_distance
        if candidate > entry_price:
            return round(candidate, 5)
        return None

    if side.upper() == "SELL":
        candidate = current_price + trail_distance
        if candidate < entry_price:
            return round(candidate, 5)
        return None

    return None
