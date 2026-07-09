"""
ctrader/auth.py
OAuth2 authentication and token refresh handling for cTrader Open API.
Keeps working with existing env vars already configured on Render.
"""
import time
import requests

from config import (
    CTRADER_CLIENT_ID,
    CTRADER_SECRET,
    CTRADER_ACCESS_TOKEN,
    CTRADER_REFRESH_TOKEN,
)

TOKEN_URL = "https://openapi.ctrader.com/apps/token"

_current_access_token = CTRADER_ACCESS_TOKEN
_current_refresh_token = CTRADER_REFRESH_TOKEN
_token_expiry = 0


def get_access_token() -> str:
    """Return a valid access token, refreshing it if it is close to expiry."""
    global _current_access_token, _token_expiry

    if _current_access_token and time.time() < _token_expiry:
        return _current_access_token

    return refresh_access_token()


def refresh_access_token() -> str:
    """Exchange the refresh token for a new access token."""
    global _current_access_token, _current_refresh_token, _token_expiry

    if not _current_refresh_token or not CTRADER_CLIENT_ID or not CTRADER_SECRET:
        return _current_access_token

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": _current_refresh_token,
        "client_id": CTRADER_CLIENT_ID,
        "client_secret": CTRADER_SECRET,
    }

    try:
        resp = requests.post(TOKEN_URL, data=payload, timeout=30)
        data = resp.json()

        if "accessToken" in data:
            _current_access_token = data["accessToken"]
            _current_refresh_token = data.get("refreshToken", _current_refresh_token)
            expires_in = data.get("expiresIn", 2592000)
            _token_expiry = time.time() + int(expires_in) - 60
        else:
            print("cTrader token refresh failed:", data)

    except Exception as exc:
        print("cTrader token refresh error:", exc)

    return _current_access_token
