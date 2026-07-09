"""market/macd.py - MACD calculation."""
import ta


def macd(series):
    indicator = ta.trend.MACD(series)
    return indicator.macd(), indicator.macd_signal(), indicator.macd_diff()
