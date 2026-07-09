"""
ctrader/market_data.py
Subscribe to and cache live spot/candle data received via the WebSocket client.
"""
from ctrader.client import client

_latest_prices = {}


def _on_message(data: dict):
    payload_type = data.get("payloadType")
    payload = data.get("payload", {})

    if payload_type == 2131:  # ProtoOASpotEvent (JSON id)
        symbol_id = payload.get("symbolId")
        bid = payload.get("bid")
        ask = payload.get("ask")
        if symbol_id is not None:
            _latest_prices[symbol_id] = {"bid": bid, "ask": ask}


client.add_listener(_on_message)


def subscribe_spots(symbol_ids: list):
    client.send({
        "payloadType": 2127,  # ProtoOASubscribeSpotsReq
        "payload": {"symbolId": symbol_ids},
    })


def get_latest_price(symbol_id: int):
    return _latest_prices.get(symbol_id)
