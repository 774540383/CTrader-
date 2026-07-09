"""
analysis/trend.py
Higher-level trend classification combining EMA and structure signals.
"""
from market.structure import detect_structure


def classify_trend(df, indicators: dict) -> str:
    structure = detect_structure(df)
    ema50 = indicators.get("EMA50", 0)
    ema200 = indicators.get("EMA200", 0)

    if structure == "UPTREND" and ema50 > ema200:
        return "STRONG_UPTREND"
    if structure == "DOWNTREND" and ema50 < ema200:
        return "STRONG_DOWNTREND"
    if ema50 > ema200:
        return "WEAK_UPTREND"
    if ema50 < ema200:
        return "WEAK_DOWNTREND"
    return "RANGING"
