"""
execution/backtest.py
Minimal backtesting harness: replays historical candles through the same
indicator/scoring pipeline used live, without calling the AI or placing
real orders. Useful groundwork for future walk-forward testing.
"""
import pandas as pd

from market.indicators import add_indicators, latest_snapshot
from analysis.scoring import compute_confluence_score


def run_backtest(historical_candles: list, min_score: int = 40) -> dict:
    """historical_candles: list of dicts with open/high/low/close/volume."""
    df = pd.DataFrame(historical_candles)
    if len(df) < 200:
        return {"error": "Not enough candles for a meaningful backtest (need >= 200)."}

    df = add_indicators(df)

    signals = []
    for i in range(200, len(df)):
        window = df.iloc[: i + 1]
        indicators = latest_snapshot(window)
        result = compute_confluence_score(window, indicators)
        if abs(result["confluence_score"]) >= min_score:
            signals.append({
                "index": i,
                "score": result["confluence_score"],
                "trend": result["trend"],
            })

    return {
        "total_candles": len(df),
        "signals_found": len(signals),
        "signals": signals[-20:],
    }
