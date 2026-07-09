"""
analysis/smart_money.py
Basic smart-money concepts: break of structure and order block detection.
"""
import pandas as pd

from market.structure import detect_structure


def detect_break_of_structure(df: pd.DataFrame, lookback: int = 30) -> str:
    if len(df) < lookback:
        return "NONE"

    structure = detect_structure(df, lookback=lookback)
    recent_close = df["close"].iloc[-1]
    recent_high = df["high"].tail(lookback).max()
    recent_low = df["low"].tail(lookback).min()

    if structure == "DOWNTREND" and recent_close > recent_high * 0.999:
        return "BULLISH_BOS"
    if structure == "UPTREND" and recent_close < recent_low * 1.001:
        return "BEARISH_BOS"
    return "NONE"


def find_order_block(df: pd.DataFrame, lookback: int = 10) -> dict:
    if len(df) < lookback:
        return {}
    window = df.tail(lookback)
    strongest_candle = window.assign(
        body=(window["close"] - window["open"]).abs()
    ).sort_values("body", ascending=False).iloc[0]
    return {
        "open": float(strongest_candle["open"]),
        "close": float(strongest_candle["close"]),
        "high": float(strongest_candle["high"]),
        "low": float(strongest_candle["low"]),
    }
