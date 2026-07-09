"""
ctrader/positions.py
Track and manage open positions reported by cTrader Open API.
"""
from config import CTRADER_ACCOUNT_ID
from ctrader.client import client
from logs.logger import get_logger

logger = get_logger("ctrader.positions")

PT_EXECUTION_EVENT = 2126
PT_RECONCILE_REQ = 2124
PT_RECONCILE_RES = 2125
PT_CLOSE_POSITION_REQ = 2111

_open_positions = {}


def _account_id() -> int:
    return int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0


def _on_message(data: dict):
    payload_type = data.get("payloadType")
    payload = data.get("payload", {})

    if payload_type == PT_EXECUTION_EVENT:
        position = payload.get("position")
        if position:
            pos_id = position.get("positionId")
            if position.get("positionStatus") == "POSITION_STATUS_CLOSED":
                _open_positions.pop(pos_id, None)
                logger.info(f"Position closed: {pos_id}")
            else:
                _open_positions[pos_id] = position
                logger.info(f"Position updated: {pos_id}")

    elif payload_type == PT_RECONCILE_RES:
        for position in payload.get("position", []):
            pos_id = position.get("positionId")
            _open_positions[pos_id] = position
        logger.info(f"Reconciled {len(_open_positions)} open positions.")


client.add_listener(_on_message)


def get_open_positions():
    return list(_open_positions.values())


def close_position(position_id: int, volume: int):
    client.send({
        "payloadType": PT_CLOSE_POSITION_REQ,
        "payload": {
            "ctidTraderAccountId": _account_id(),
            "positionId": position_id,
            "volume": volume,
        },
    })


def request_reconcile():
    client.send({
        "payloadType": PT_RECONCILE_REQ,
        "payload": {"ctidTraderAccountId": _account_id()},
    })
