"""
ctrader/positions.py
Track and manage open positions reported by cTrader Open API.
"""
from ctrader.client import client

_open_positions = {}


def _on_message(data: dict):
    payload_type = data.get("payloadType")
    payload = data.get("payload", {})

    if payload_type == 2135:  # ProtoOAExecutionEvent
        position = payload.get("position")
        if position:
            pos_id = position.get("positionId")
            _open_positions[pos_id] = position


client.add_listener(_on_message)


def get_open_positions():
    return list(_open_positions.values())


def close_position(position_id: int, volume: int):
    client.send({
        "payloadType": 2107,  # ProtoOAClosePositionReq
        "payload": {"positionId": position_id, "volume": volume},
    })
