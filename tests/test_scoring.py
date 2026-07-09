"""
tests/test_scoring.py
Unit tests for the confluence scoring engine using synthetic candle data.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from market.indicators import add_indicators, latest_snapshot
from analysis.scoring import compute_confluence_score


def _make_synthetic_df(n=250):
    data = []
    price = 2000.0
    for i in range(n):
        price += 0.5
        data.append({
            "open": price,
            "high": price + 1,
            "low": price - 1,
            "close": price + 0.3,
            "volume": 100,
        })
    return pd.DataFrame(data)


def test_confluence_score_runs_without_error():
    df = _make_synthetic_df()
    df = add_indicators(df)
    indicators = latest_snapshot(df)
    result = compute_confluence_score(df, indicators)
    assert "confluence_score" in result
    assert "trend" in result
