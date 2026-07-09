"""
ctrader/client.py
Outbound WebSocket connection to cTrader Open API (JSON protocol, port 5036).
Implements the full handshake: ProtoOAApplicationAuthReq -> ProtoOAAccountAuthReq,
and exposes a `ready` flag that becomes True only after both steps succeed.
Designed for Render (outbound-only connections, no inbound listener required).
"""
import json
import asyncio
import threading
import time

import websockets

from config import CTRADER_ACCOUNT_ID, CTRADER_CLIENT_ID, CTRADER_SECRET, CTRADER_USE_LIVE
from ctrader.auth import get_access_token
from logs.logger import get_logger

logger = get_logger("ctrader.client")

DEMO_HOST = "wss://demo.ctraderapi.com:5036"
LIVE_HOST = "wss://live.ctraderapi.com:5036"

# Correct ProtoOAPayloadType values (spotware/openapi-proto-messages)
PT_APPLICATION_AUTH_REQ = 2100
PT_APPLICATION_AUTH_RES = 2101
PT_ACCOUNT_AUTH_REQ = 2102
PT_ACCOUNT_AUTH_RES = 2103
PT_ERROR_RES = 2142


class CTraderClient:
    def __init__(self, use_live: bool = None):
        use_live = CTRADER_USE_LIVE if use_live is None else use_live
        self.host = LIVE_HOST if use_live else DEMO_HOST
        self.ws = None
        self.connected = False
        self.app_authenticated = False
        self.account_authenticated = False
        self._loop = None
        self._listeners = []

    @property
    def ready(self) -> bool:
        return self.connected and self.app_authenticated and self.account_authenticated

    def add_listener(self, callback):
        self._listeners.append(callback)

    async def _connect(self):
        self.ws = await websockets.connect(self.host, ping_interval=20)
        self.connected = True
        self.app_authenticated = False
        self.account_authenticated = False

        if not CTRADER_CLIENT_ID or not CTRADER_SECRET:
            logger.error("Missing CTRADER_CLIENT_ID/CTRADER_SECRET - cannot authenticate application.")
            return

        await self.ws.send(json.dumps({
            "payloadType": PT_APPLICATION_AUTH_REQ,
            "payload": {
                "clientId": CTRADER_CLIENT_ID,
                "clientSecret": CTRADER_SECRET,
            },
        }))

    async def _send_account_auth(self):
        account_id = int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0
        await self.ws.send(json.dumps({
            "payloadType": PT_ACCOUNT_AUTH_REQ,
            "payload": {
                "ctidTraderAccountId": account_id,
                "accessToken": get_access_token(),
            },
        }))

    async def _listen(self):
        async for message in self.ws:
            try:
                data = json.loads(message)
            except Exception:
                continue

            payload_type = data.get("payloadType")

            if payload_type == PT_APPLICATION_AUTH_RES:
                self.app_authenticated = True
                logger.info("cTrader application authenticated.")
                await self._send_account_auth()

            elif payload_type == PT_ACCOUNT_AUTH_RES:
                self.account_authenticated = True
                logger.info("cTrader account authenticated. Client is READY.")

            elif payload_type == PT_ERROR_RES:
                logger.error(f"cTrader API error: {data.get('payload')}")

            for cb in self._listeners:
                try:
                    cb(data)
                except Exception as exc:
                    logger.error(f"Listener error: {exc}")

    async def _run(self):
        while True:
            try:
                await self._connect()
                await self._listen()
            except Exception as exc:
                logger.error(f"cTrader WS error, reconnecting in 5s: {exc}")
                self.connected = False
                self.app_authenticated = False
                self.account_authenticated = False
                await asyncio.sleep(5)

    def start(self):
        """Start the WebSocket client on a background thread/event loop."""
        def _runner():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._run())

        thread = threading.Thread(target=_runner, daemon=True)
        thread.start()

    def wait_until_ready(self, timeout: float = 20.0) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            if self.ready:
                return True
            time.sleep(0.5)
        return self.ready

    def send(self, payload: dict):
        if self.ws and self.connected and self._loop:
            asyncio.run_coroutine_threadsafe(
                self.ws.send(json.dumps(payload)), self._loop
            )
        else:
            logger.warning(f"send() called before connection ready, dropping payload: {payload.get('payloadType')}")


client = CTraderClient()
