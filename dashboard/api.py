"""
dashboard/api.py
FastAPI router exposing dashboard data: balance, open positions, trade
history, win rate, and AI status. Included into main.py without altering
existing routes.
"""
from fastapi import APIRouter

from ctrader.account import get_account_info
from ctrader.positions import get_open_positions
from database.history import get_trade_history
from risk.daily_loss import get_daily_loss_percent
from ai.memory import get_recent_history

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary():
    history = get_trade_history(limit=50)
    closed = [t for t in history if t["status"] == "CLOSED"]
    wins = [t for t in closed if (t.get("pnl") or 0) > 0]
    win_rate = round((len(wins) / len(closed)) * 100, 2) if closed else 0.0

    return {
        "account": get_account_info(),
        "open_positions": get_open_positions(),
        "daily_loss_percent": get_daily_loss_percent(),
        "win_rate": win_rate,
        "recent_trades": history[:10],
        "ai_recent_decisions": get_recent_history(),
    }


@router.get("/trades")
def trades(limit: int = 50):
    return {"trades": get_trade_history(limit=limit)}
