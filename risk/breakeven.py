"""
risk/breakeven.py
Move stop-loss to breakeven once a trade reaches a defined profit threshold.
"""


def should_move_to_breakeven(entry_price: float, current_price: float, side: str,
                              trigger_distance: float) -> bool:
    if side.upper() == "BUY":
        return (current_price - entry_price) >= trigger_distance
    if side.upper() == "SELL":
        return (entry_price - current_price) >= trigger_distance
    return False


def breakeven_price(entry_price: float, buffer_pips: float = 0.0, side: str = "BUY") -> float:
    if side.upper() == "BUY":
        return round(entry_price + buffer_pips, 5)
    return round(entry_price - buffer_pips, 5)
