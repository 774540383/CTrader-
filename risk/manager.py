"""
risk/manager.py
Smart Risk Manager: final gatekeeper before any trade decision is accepted.
"""
from config import MAX_POSITIONS
from risk.position_size import calculate_position_size
from risk.protection import is_in_cooldown
from ctrader.positions import get_open_positions


def evaluate_risk(decision: dict, market_data: dict) -> dict:
    """Adjust or reject an AI decision based on account-level risk rules."""
    if decision.get("decision") == "WAIT":
        return decision

    if is_in_cooldown():
        decision["decision"] = "WAIT"
        decision["risk_warning"] = "Cooldown active after recent loss."
        return decision

    open_positions = get_open_positions()
    if len(open_positions) >= MAX_POSITIONS:
        decision["decision"] = "WAIT"
        decision["risk_warning"] = f"Max positions ({MAX_POSITIONS}) reached."
        return decision

    if decision.get("confidence", 0) < 85:
        decision["decision"] = "WAIT"
        decision["risk_warning"] = "Confidence below threshold."
        return decision

    decision["approved_position_size"] = calculate_position_size(
        account_balance=market_data.get("account_balance", 1000),
        stop_loss_pips=market_data.get("stop_loss_pips", 50),
    )
    return decision
