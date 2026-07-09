"""
ctrader/symbols.py
Symbol metadata cache (symbol name <-> symbolId mapping).
"""
from ctrader.client import client

_symbols = {}


def _on_message(data: dict):
    if data.get("payloadType") == 2115:  # ProtoOASymbolsListRes
        for sym in data.get("payload", {}).get("symbol", []):
            _symbols[sym.get("symbolName")] = sym.get("symbolId")


client.add_listener(_on_message)


def get_symbol_id(name: str) -> int:
    return _symbols.get(name, 1)  # default fallback for XAUUSD in dev/paper mode


def request_symbols_list(account_id: int):
    client.send({
        "payloadType": 2114,  # ProtoOASymbolsListReq
        "payload": {"ctidTraderAccountId": account_id},
    })
