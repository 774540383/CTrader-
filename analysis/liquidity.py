"""
analysis/liquidity.py
Detect liquidity pools (equal highs/lows) that price is likely to sweep.
"""
import pandas as pd

_TOLERANCE = 0.0005  # 0.05% price tolerance for "equal" levels


def find_liquidity_pools(df: pd.DataFrame, lookback: int = 50) -> dict:
    if len(df) < lookback:
        return {"equal_highs": [], "equal_lows": []}

    window = df.tail(lookback)
    highs = window["high"].round(2)
    lows = window["low"].round(2)

    equal_highs = highs[highs.duplicated(keep=False)].unique().tolist()
    equal_lows = lows[lows.duplicated(keep=False)].unique().tolist()

    return {"equal_highs": equal_highs, "equal_lows": equal_lows}
