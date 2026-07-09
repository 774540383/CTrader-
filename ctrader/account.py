"""
ctrader/account.py
Trader account info: balance, equity, margin - cached from account events.
"""
from ctrader.client import client
from config import CTRADER_ACCOUNT_ID
from logs.logger import get_logger

logger = get_logger("ctrader.account")

PT_TRADER_REQ = 2121
PT_TRADER_RES = 2122
PT_TRADER_UPDATE_EVENT = 2123

_account_info = {"balance": 0.0, "equity": 0.0, "margin": 0.0}
MONEY_SCALE = 100.0


def _apply_trader(trader: dict):
    if not trader:
        return
    balance = trader.get("balance", 0) / MONEY_SCALE
    _account_info["balance"] = balance
    _account_info["equity"] = balance
    _account_info["margin"] = trader.get("usedMargin", 0) / MONEY_SCALE
    logger.info(f"Account info updated: {_account_info}")


def _on_message(data: dict):
    payload_type = data.get("payloadType")
    if payload_type in (PT_TRADER_RES, PT_TRADER_UPDATE_EVENT):
        _apply_trader(data.get("payload", {}).get("trader", {}))


client.add_listener(_on_message)


def get_account_info() -> dict:
    return dict(_account_info)


def request_trader_info(account_id: int = None):
    acc = account_id if account_id is not None else (int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0)
    client.send({
        "payloadType": PT_TRADER_REQ,
        "payload": {"ctidTraderAccountId": acc},
    })
