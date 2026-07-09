"""market/rsi.py - RSI calculation."""
import ta


def rsi(series, window: int = 14):
    return ta.momentum.RSIIndicator(series, window=window).rsi()
