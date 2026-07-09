"""market/atr.py - ATR calculation."""
import ta


def atr(high, low, close, window: int = 14):
    return ta.volatility.AverageTrueRange(high, low, close, window=window).average_true_range()
