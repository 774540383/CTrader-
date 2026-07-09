"""
market/supply_demand.py
Basic supply/demand zone detection using swing highs/lows.
"""
import pandas as pd


def find_zones(df: pd.DataFrame, lookback: int = 50) -> dict:
    if len(df) < lookback:
        return {"supply": None, "demand": None}
    window = df.tail(lookback)
    supply = float(window["high"].max())
    demand = float(window["low"].min())
    return {"supply": supply, "demand": demand}
