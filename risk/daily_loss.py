"""
risk/daily_loss.py
Dedicated daily loss tracking, separate from the general protection module
so it can be queried directly by the dashboard/API.
"""
import time
from datetime import datetime, timezone

_state = {"date": None, "loss": 0.0, "starting_balance": 0.0}


def _reset_if_new_day():
    today = datetime.now(timezone.utc).date()
    if _state["date"] != today:
        _state["date"] = today
        _state["loss"] = 0.0


def set_starting_balance(balance: float):
    _reset_if_new_day()
    _state["starting_balance"] = balance


def register_loss(amount: float):
    _reset_if_new_day()
    if amount < 0:
        _state["loss"] += abs(amount)


def get_daily_loss_percent() -> float:
    _reset_if_new_day()
    if _state["starting_balance"] <= 0:
        return 0.0
    return round((_state["loss"] / _state["starting_balance"]) * 100, 2)


def get_state() -> dict:
    _reset_if_new_day()
    return dict(_state)
