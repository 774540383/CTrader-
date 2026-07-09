"""
ctrader/symbols.py
Symbol metadata cache (symbol name <-> symbolId mapping).
"""
from ctrader.client import client
from config import CTRADER_ACCOUNT_ID
from logs.logger import get_logger

logger = get_logger("ctrader.symbols")

PT_SYMBOLS_LIST_REQ = 2114
PT_SYMBOLS_LIST_RES = 2115

_symbols = {}
_DEFAULT_XAUUSD_ID = 41  # common cTrader XAUUSD symbolId, overwritten once real list arrives


def _on_message(data: dict):
    if data.get("payloadType") == PT_SYMBOLS_LIST_RES:
        for sym in data.get("payload", {}).get("symbol", []):
            name = sym.get("symbolName")
            sid = sym.get("symbolId")
            if name and sid:
                _symbols[name] = sid
        if _symbols:
            logger.info(f"Loaded {len(_symbols)} symbols from cTrader.")


client.add_listener(_on_message)


def get_symbol_id(name: str) -> int:
    return _symbols.get(name, _DEFAULT_XAUUSD_ID)


def request_symbols_list(account_id: int = None):
    acc = account_id if account_id is not None else (int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0)
    client.send({
        "payloadType": PT_SYMBOLS_LIST_REQ,
        "payload": {"ctidTraderAccountId": acc},
    })
