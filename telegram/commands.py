"""
telegram/commands.py
Command definitions used by telegram/bot.py, kept separate for clarity and
future extension (e.g. /pause, /resume, /report).
"""
from database.history import get_trade_history
from risk.daily_loss import get_daily_loss_percent


def cmd_status() -> str:
    from risk.protection import is_in_cooldown
    cooldown = "YES" if is_in_cooldown() else "NO"
    daily_loss = get_daily_loss_percent()
    return f"Bot running.\nCooldown: {cooldown}\nDaily loss: {daily_loss}%"


def cmd_history() -> str:
    trades = get_trade_history(limit=10)
    if not trades:
        return "No trade history yet."
    lines = [f"{t['symbol']} {t['side']} vol={t['volume']} status={t['status']}" for t in trades]
    return "\n".join(lines)


def cmd_help() -> str:
    return "Commands: /status, /positions, /history, /help"
