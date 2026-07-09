"""market/ema.py - EMA calculation."""
import ta


def ema(series, window: int):
    return ta.trend.EMAIndicator(series, window=window).ema_indicator()
