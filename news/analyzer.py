"""
news/analyzer.py
News Filter: determines whether trading should pause due to high-impact
economic news within a short window of the current time.
"""
import time
from datetime import datetime, timezone

from news.calendar import get_upcoming_events

HIGH_IMPACT_WINDOW_MINUTES = 30


def get_news_risk(symbol: str = "XAUUSD") -> str:
    """Return 'HIGH', 'MEDIUM', or 'LOW' news risk for the relevant currency."""
    currency = "USD"  # XAUUSD is primarily driven by USD news
    events = get_upcoming_events(currency)

    if not events:
        return "LOW"

    now = datetime.now(timezone.utc)

    for event in events:
        impact = str(event.get("impact", "")).lower()
        if impact != "high":
            continue

        event_time_str = event.get("date")
        if not event_time_str:
            continue

        try:
            event_time = datetime.fromisoformat(event_time_str.replace("Z", "+00:00"))
        except Exception:
            continue

        minutes_diff = abs((event_time - now).total_seconds()) / 60
        if minutes_diff <= HIGH_IMPACT_WINDOW_MINUTES:
            return "HIGH"

    return "LOW"
