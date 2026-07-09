"""
risk/position_size.py
Position sizing based on account risk percentage and stop-loss distance.
"""
from config import RISK_PERCENT


def calculate_position_size(account_balance: float, stop_loss_pips: float,
                             pip_value: float = 1.0) -> float:
    """Return position size (lots) so that a stop-loss hit risks RISK_PERCENT of balance."""
    if stop_loss_pips <= 0 or account_balance <= 0:
        return 0.0

    risk_amount = account_balance * (RISK_PERCENT / 100)
    lots = risk_amount / (stop_loss_pips * pip_value)
    return round(max(lots, 0.0), 2)
