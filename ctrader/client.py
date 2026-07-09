"""
ctrader/client.py
Outbound WebSocket connection to cTrader Open API (JSON protocol, port 5036).
Designed for Render (outbound-only connections, no inbound listener required).
"""
import json
import asyncio
import threading

import websockets

from config import CTRADER_ACCOUNT_ID
from ctrader.auth import get_access_token

DEMO_HOST = "wss://demo.ctraderapi.com:5036"
LIVE_HOST = "wss://live.ctraderapi.com:5036"


class CTraderClient:
    def __init__(self, use_live: bool = False):
        self.host = LIVE_HOST if use_live else DEMO_HOST
        self.ws = None
        self.connected = False
        self._lock = threading.Lock()
        self._loop = None
        self._listeners = []

    def add_listener(self, callback):
        self._listeners.append(callback)

    async def _connect(self):
        self.ws = await websockets.connect(self.host, ping_interval=20)
        self.connected = True

        auth_req = {
            "payloadType": 2100,
            "payload": {
                "clientId": "",
                "clientSecret": "",
            },
        }
        # Application auth is optional if account auth token already scoped.
        account_auth = {
            "payloadType": 2102,
            "payload": {
                "ctidTraderAccountId": int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0,
                "accessToken": get_access_token(),
            },
        }
        await self.ws.send(json.dumps(account_auth))

    async def _listen(self):
        async for message in self.ws:
            try:
                data = json.loads(message)
            except Exception:
                continue
            for cb in self._listeners:
                try:
                    cb(data)
                except Exception as exc:
                    print("Listener error:", exc)

    async def _run(self):
        while True:
            try:
                await self._connect()
                await self._listen()
            except Exception as exc:
                print("cTrader WS error, reconnecting in 5s:", exc)
                self.connected = False
                await asyncio.sleep(5)

    def start(self):
        """Start the WebSocket client on a background thread/event loop."""
        def _runner():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._run())

        thread = threading.Thread(target=_runner, daemon=True)
        thread.start()

    def send(self, payload: dict):
        if self.ws and self.connected and self._loop:
            asyncio.run_coroutine_threadsafe(
                self.ws.send(json.dumps(payload)), self._loop
            )


client = CTraderClient()
