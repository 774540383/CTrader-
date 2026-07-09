"""
ctrader/websocket.py
Thin wrapper module documenting/exposing the WebSocket connection used by
ctrader/client.py. Kept separate to match the requested project layout and
to allow swapping JSON <-> Protobuf transport without touching client.py.
"""
from ctrader.client import CTraderClient, DEMO_HOST, LIVE_HOST

__all__ = ["CTraderClient", "DEMO_HOST", "LIVE_HOST"]
