"""
market/indicators.py
Technical indicator calculations built on top of pandas/ta.
"""
import pandas as pd
import ta


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add RSI, EMA50, EMA200, ATR, and MACD columns to a candle DataFrame."""
    df = df.copy()
    df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    df["EMA50"] = ta.trend.EMAIndicator(df["close"], window=50).ema_indicator()
    df["EMA200"] = ta.trend.EMAIndicator(df["close"], window=200).ema_indicator()
    df["ATR"] = ta.volatility.AverageTrueRange(
        df["high"], df["low"], df["close"], window=14
    ).average_true_range()
    macd = ta.trend.MACD(df["close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    return df


def latest_snapshot(df: pd.DataFrame) -> dict:
    """Return the most recent indicator values as a plain dict for the AI prompt."""
    if df.empty:
        return {}
    last = df.iloc[-1]
    return {
        "RSI": round(float(last.get("RSI", 0)), 2),
        "EMA50": round(float(last.get("EMA50", 0)), 5),
        "EMA200": round(float(last.get("EMA200", 0)), 5),
        "ATR": round(float(last.get("ATR", 0)), 5),
        "MACD": round(float(last.get("MACD", 0)), 5),
        "MACD_signal": round(float(last.get("MACD_signal", 0)), 5),
    }
