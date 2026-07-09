"""
ctrader/orders.py
Order execution helpers (market orders with SL/TP) via cTrader Open API.
"""
from config import CTRADER_ACCOUNT_ID, PAPER_TRADING
from ctrader.client import client
from logs.logger import get_logger

logger = get_logger("ctrader.orders")

PT_NEW_ORDER_REQ = 2106


def send_market_order(symbol_id: int, volume: int, side: str,
                       stop_loss: float = None, take_profit: float = None):
    """side: 'BUY' or 'SELL'. volume is in 0.01 units (cTrader convention,
    e.g. 100000 = 1.00 lot for most FX/metals symbols)."""
    if PAPER_TRADING:
        logger.info(f"PAPER TRADE: {side} {symbol_id} vol={volume} SL={stop_loss} TP={take_profit}")
        return {"status": "PAPER_TRADE", "symbol_id": symbol_id, "side": side, "volume": volume}

    if not client.ready:
        logger.error("Order rejected: cTrader client not ready (not authenticated).")
        return {"status": "REJECTED", "reason": "Client not authenticated"}

    account_id = int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0

    payload = {
        "payloadType": PT_NEW_ORDER_REQ,
        "payload": {
            "ctidTraderAccountId": account_id,
            "symbolId": symbol_id,
            "orderType": "MARKET",
            "tradeSide": side.upper(),
            "volume": volume,
            "timeInForce": "IMMEDIATE_OR_CANCEL",
        },
    }
    if stop_loss:
        payload["payload"]["stopLoss"] = stop_loss
    if take_profit:
        payload["payload"]["takeProfit"] = take_profit

    client.send(payload)
    logger.info(f"LIVE ORDER SENT: {side} {symbol_id} vol={volume} SL={stop_loss} TP={take_profit}")
    return {"status": "SENT", "symbol_id": symbol_id, "side": side, "volume": volume}
