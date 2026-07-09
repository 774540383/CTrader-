"""
risk/protection.py
Account-level protection rules: max daily loss, max drawdown, cooldowns.
"""
import time

_daily_loss = 0.0
_last_loss_time = 0
_COOLDOWN_SECONDS = 900

MAX_DAILY_LOSS_PERCENT = 5.0


def register_trade_result(pnl: float, account_balance: float):
    global _daily_loss, _last_loss_time
    if pnl < 0:
        _daily_loss += abs(pnl)
        _last_loss_time = time.time()
    _check_daily_limit(account_balance)


def _check_daily_limit(account_balance: float):
    if account_balance <= 0:
        return
    loss_percent = (_daily_loss / account_balance) * 100
    if loss_percent >= MAX_DAILY_LOSS_PERCENT:
        print("MAX DAILY LOSS REACHED - trading should halt.")


def is_in_cooldown() -> bool:
    return (time.time() - _last_loss_time) < _COOLDOWN_SECONDS


def reset_daily_loss():
    global _daily_loss
    _daily_loss = 0.0
