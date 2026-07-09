"""
ctrader/market_data.py
Subscribe to and cache live spot/candle data received via the WebSocket client.
Also feeds the in-memory candle buffer (market/candles.py) from live and
historical trend bars, so the AI/technical-analysis pipeline always has
real data to work with.
"""
import time as _time

from ctrader.client import client
from config import CTRADER_ACCOUNT_ID
from market.candles import add_candle
from logs.logger import get_logger

logger = get_logger("ctrader.market_data")

PT_SUBSCRIBE_SPOTS_REQ = 2127
PT_SPOT_EVENT = 2131
PT_SUBSCRIBE_LIVE_TRENDBAR_REQ = 2135
PT_GET_TRENDBARS_REQ = 2137
PT_GET_TRENDBARS_RES = 2138

_latest_prices = {}

# cTrader prices are transmitted as integers scaled by 1/100000
PRICE_SCALE = 100000.0


def _account_id() -> int:
    return int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0


def _trendbar_to_candle(tb: dict) -> dict:
    low = tb.get("low", 0) / PRICE_SCALE
    delta_open = tb.get("deltaOpen", 0) / PRICE_SCALE
    delta_high = tb.get("deltaHigh", 0) / PRICE_SCALE
    delta_close = tb.get("deltaClose", 0) / PRICE_SCALE
    return {
        "time": tb.get("utcTimestampInMinutes"),
        "open": low + delta_open,
        "high": low + delta_high,
        "low": low,
        "close": low + delta_close,
        "volume": tb.get("volume", 0),
    }


def _on_message(data: dict):
    payload_type = data.get("payloadType")
    payload = data.get("payload", {})

    if payload_type == PT_SPOT_EVENT:
        symbol_id = payload.get("symbolId")
        bid = payload.get("bid")
        ask = payload.get("ask")

        if symbol_id is not None:
            price_entry = _latest_prices.get(symbol_id, {})
            if bid is not None:
                price_entry["bid"] = bid / PRICE_SCALE
            if ask is not None:
                price_entry["ask"] = ask / PRICE_SCALE
            if price_entry:
                _latest_prices[symbol_id] = price_entry

        for tb in payload.get("trendbar", []):
            add_candle("XAUUSD", _trendbar_to_candle(tb))

    elif payload_type == PT_GET_TRENDBARS_RES:
        trendbars = payload.get("trendbar", [])
        for tb in trendbars:
            add_candle("XAUUSD", _trendbar_to_candle(tb))
        logger.info(f"Loaded {len(trendbars)} historical candles.")


client.add_listener(_on_message)


def subscribe_spots(symbol_ids: list):
    client.send({
        "payloadType": PT_SUBSCRIBE_SPOTS_REQ,
        "payload": {
            "ctidTraderAccountId": _account_id(),
            "symbolId": symbol_ids,
            "subscribeToSpotTimestamp": True,
        },
    })
    logger.info(f"Subscribed to spots for symbol ids: {symbol_ids}")


def subscribe_live_trendbars(symbol_id: int, period: str = "M5"):
    client.send({
        "payloadType": PT_SUBSCRIBE_LIVE_TRENDBAR_REQ,
        "payload": {
            "ctidTraderAccountId": _account_id(),
            "period": period,
            "symbolId": symbol_id,
        },
    })
    logger.info(f"Subscribed to live {period} trendbars for symbol id: {symbol_id}")


def request_historical_trendbars(symbol_id: int, account_id: int = None, count: int = 300, period: str = "M5"):
    now_ms = int(_time.time() * 1000)
    from_ms = now_ms - (count * 5 * 60 * 1000)
    client.send({
        "payloadType": PT_GET_TRENDBARS_REQ,
        "payload": {
            "ctidTraderAccountId": account_id if account_id is not None else _account_id(),
            "fromTimestamp": from_ms,
            "toTimestamp": now_ms,
            "period": period,
            "symbolId": symbol_id,
            "count": count,
        },
    })
    logger.info(f"Requested {count} historical {period} trendbars for symbol id: {symbol_id}")


def get_latest_price(symbol_id: int):
    return _latest_prices.get(symbol_id)


def get_mid_price(symbol_id: int):
    entry = _latest_prices.get(symbol_id)
    if not entry:
        return None
    bid = entry.get("bid")
    ask = entry.get("ask")
    if bid is not None and ask is not None:
        return round((bid + ask) / 2, 5)
    return bid or ask
