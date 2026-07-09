"""
analysis/scoring.py
Combine trend, volatility, liquidity, and price action signals into a
single confluence score used to sanity-check the AI decision.
"""
from analysis.trend import classify_trend
from analysis.volatility import classify_volatility
from analysis.liquidity import find_liquidity_pools
from market.price_action import detect_pin_bar, detect_engulfing


def compute_confluence_score(df, indicators: dict) -> dict:
    trend = classify_trend(df, indicators)
    volatility = classify_volatility(df)
    liquidity = find_liquidity_pools(df)
    engulfing = detect_engulfing(df)
    pin_bar = detect_pin_bar(df)

    score = 0
    if "UPTREND" in trend:
        score += 30
    if "DOWNTREND" in trend:
        score -= 30
    if engulfing == "BULLISH":
        score += 20
    if engulfing == "BEARISH":
        score -= 20
    if pin_bar:
        score += 10 if score >= 0 else -10
    if volatility == "HIGH":
        score = int(score * 0.7)  # reduce confidence in high volatility

    return {
        "trend": trend,
        "volatility": volatility,
        "liquidity": liquidity,
        "engulfing": engulfing,
        "pin_bar": pin_bar,
        "confluence_score": score,
    }
