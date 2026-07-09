"""market/bollinger.py - Bollinger Bands calculation."""
import ta


def bollinger_bands(series, window: int = 20, window_dev: int = 2):
    bb = ta.volatility.BollingerBands(series, window=window, window_dev=window_dev)
    return bb.bollinger_hband(), bb.bollinger_mavg(), bb.bollinger_lband()
