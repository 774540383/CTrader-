"""
market/price_action.py
Simple price action pattern detection (engulfing, pin bar).
"""
import pandas as pd


def detect_pin_bar(df: pd.DataFrame) -> bool:
    if len(df) < 1:
        return False
    last = df.iloc[-1]
    body = abs(last["close"] - last["open"])
    candle_range = last["high"] - last["low"]
    if candle_range == 0:
        return False
    return (body / candle_range) < 0.3


def detect_engulfing(df: pd.DataFrame) -> str:
    if len(df) < 2:
        return "NONE"
    prev, last = df.iloc[-2], df.iloc[-1]
    bullish = last["close"] > last["open"] and prev["close"] < prev["open"] \
        and last["close"] > prev["open"] and last["open"] < prev["close"]
    bearish = last["close"] < last["open"] and prev["close"] > prev["open"] \
        and last["open"] > prev["close"] and last["close"] < prev["open"]
    if bullish:
        return "BULLISH"
    if bearish:
        return "BEARISH"
    return "NONE"
