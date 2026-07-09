"""
ctrader/orders.py
Order execution helpers (market orders with SL/TP) via cTrader Open API.
"""
from config import CTRADER_ACCOUNT_ID, PAPER_TRADING
from ctrader.client import client


def send_market_order(symbol_id: int, volume: int, side: str,
                       stop_loss: float = None, take_profit: float = None):
    """side: 'BUY' or 'SELL'. volume is in lots * 100 (cTrader units)."""
    if PAPER_TRADING:
        return {"status": "PAPER_TRADE", "symbol_id": symbol_id, "side": side, "volume": volume}

    order_type = 1 if side.upper() == "BUY" else 2
    payload = {
        "payloadType": 2106,  # ProtoOANewOrderReq
        "payload": {
            "ctidTraderAccountId": int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0,
            "symbolId": symbol_id,
            "orderType": "MARKET",
            "tradeSide": "BUY" if order_type == 1 else "SELL",
            "volume": volume,
            "stopLoss": stop_loss,
            "takeProfit": take_profit,
        },
    }
    client.send(payload)
    return {"status": "SENT", "symbol_id": symbol_id, "side": side, "volume": volume}
