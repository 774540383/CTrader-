"""
analysis/volume.py
Volume-based analysis: relative volume spikes vs recent average.
"""
import pandas as pd


def relative_volume(df: pd.DataFrame, window: int = 20) -> float:
    if "volume" not in df.columns or len(df) < window:
        return 1.0
    avg_volume = df["volume"].tail(window).mean()
    if avg_volume == 0:
        return 1.0
    last_volume = df["volume"].iloc[-1]
    return round(float(last_volume / avg_volume), 2)


def is_volume_spike(df: pd.DataFrame, threshold: float = 1.8) -> bool:
    return relative_volume(df) >= threshold
