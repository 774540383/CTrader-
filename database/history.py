"""
database/history.py
Persistence helpers for trade decisions and executed trades.
"""
from database.database import session_scope
from database.models import TradeDecision, Trade


def save_decision(decision: dict, symbol: str):
    with session_scope() as session:
        record = TradeDecision(
            symbol=symbol,
            decision=decision.get("decision"),
            confidence=decision.get("confidence", 0),
            entry_reason=decision.get("entry_reason", ""),
            risk_warning=decision.get("risk_warning", ""),
            raw_response=str(decision),
        )
        session.add(record)


def save_trade(symbol: str, side: str, volume: float, entry_price: float = None,
               stop_loss: float = None, take_profit: float = None, position_id: int = None):
    with session_scope() as session:
        trade = Trade(
            position_id=position_id,
            symbol=symbol,
            side=side,
            volume=volume,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            status="OPEN",
        )
        session.add(trade)


def get_trade_history(limit: int = 50) -> list:
    with session_scope() as session:
        trades = session.query(Trade).order_by(Trade.opened_at.desc()).limit(limit).all()
        return [
            {
                "id": t.id,
                "symbol": t.symbol,
                "side": t.side,
                "volume": t.volume,
                "status": t.status,
                "pnl": t.pnl,
            }
            for t in trades
        ]
