"""
market/candles.py
In-memory OHLC candle buffer, fed by live spot data or historical fetch.
"""
import pandas as pd

_MAX_CANDLES = 500
_candles = {}


def add_candle(symbol: str, candle: dict):
    """candle: {time, open, high, low, close, volume}"""
    buf = _candles.setdefault(symbol, [])
    buf.append(candle)
    if len(buf) > _MAX_CANDLES:
        buf.pop(0)


def get_dataframe(symbol: str) -> pd.DataFrame:
    buf = _candles.get(symbol, [])
    if not buf:
        return pd.DataFrame(columns=["time", "open", "high", "low", "close", "volume"])
    return pd.DataFrame(buf)
