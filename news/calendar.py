"""
news/calendar.py
Lightweight economic calendar fetcher. Falls back gracefully if no API key
is configured, so the bot keeps working with a neutral news assumption.
"""
import time
import requests

_CACHE = {"data": None, "ts": 0}
_CACHE_TTL = 900  # 15 minutes


def get_upcoming_events(currency: str = "USD") -> list:
    now = time.time()
    if _CACHE["data"] and (now - _CACHE["ts"]) < _CACHE_TTL:
        return _CACHE["data"]

    events = []
    try:
        resp = requests.get(
            "https://nfs.faireconomy.media/ff_calendar_thisweek.json",
            timeout=10,
        )
        if resp.status_code == 200:
            all_events = resp.json()
            events = [e for e in all_events if e.get("country") == currency]
    except Exception as exc:
        print("Calendar fetch failed, defaulting to no known events:", exc)
        events = []

    _CACHE["data"] = events
    _CACHE["ts"] = now
    return events
