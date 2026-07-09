"""
market/structure.py
Market structure detection: higher highs/lows vs lower highs/lows.
"""
import pandas as pd


def detect_structure(df: pd.DataFrame, lookback: int = 20) -> str:
    if len(df) < lookback:
        return "UNKNOWN"
    window = df.tail(lookback)
    highs = window["high"].values
    lows = window["low"].values

    higher_highs = all(highs[i] <= highs[i + 1] for i in range(len(highs) - 3, len(highs) - 1))
    higher_lows = all(lows[i] <= lows[i + 1] for i in range(len(lows) - 3, len(lows) - 1))
    lower_highs = all(highs[i] >= highs[i + 1] for i in range(len(highs) - 3, len(highs) - 1))
    lower_lows = all(lows[i] >= lows[i + 1] for i in range(len(lows) - 3, len(lows) - 1))

    if higher_highs and higher_lows:
        return "UPTREND"
    if lower_highs and lower_lows:
        return "DOWNTREND"
    return "RANGING"
