"""
analysis/volatility.py
Volatility classification based on ATR relative to recent average.
"""
import pandas as pd


def classify_volatility(df: pd.DataFrame, atr_column: str = "ATR") -> str:
    if atr_column not in df.columns or len(df) < 20:
        return "UNKNOWN"

    recent_atr = df[atr_column].tail(5).mean()
    baseline_atr = df[atr_column].tail(50).mean()

    if baseline_atr == 0 or pd.isna(baseline_atr):
        return "UNKNOWN"

    ratio = recent_atr / baseline_atr
    if ratio > 1.5:
        return "HIGH"
    if ratio < 0.7:
        return "LOW"
    return "NORMAL"
