"""
ctrader/account.py
Trader account info: balance, equity, margin - cached from account events.
"""
from ctrader.client import client

_account_info = {"balance": 0.0, "equity": 0.0, "margin": 0.0}


def _on_message(data: dict):
    if data.get("payloadType") == 2121:  # ProtoOATraderRes
        trader = data.get("payload", {}).get("trader", {})
        if trader:
            _account_info["balance"] = trader.get("balance", 0) / 100
            _account_info["equity"] = trader.get("balance", 0) / 100
            _account_info["margin"] = trader.get("usedMargin", 0) / 100


client.add_listener(_on_message)


def get_account_info() -> dict:
    return dict(_account_info)


def request_trader_info(account_id: int):
    client.send({
        "payloadType": 2120,  # ProtoOATraderReq
        "payload": {"ctidTraderAccountId": account_id},
    })
