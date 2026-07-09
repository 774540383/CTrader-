"""
ai/decision_engine.py
Central AI Decision Engine: combines live market data, technical analysis,
risk context and news filter into a single trading decision via OpenRouter.
"""
from ai.openrouter_client import analyze_market
from ai.model_selector import select_model
from ai.memory import record_decision, summarize_recent
from risk.manager import evaluate_risk
from news.analyzer import get_news_risk


def make_decision(market_data: dict) -> dict:
    """Full pipeline: enrich data -> AI analysis -> risk review -> final decision."""
    news_risk = get_news_risk(market_data.get("symbol", "XAUUSD"))
    market_data = dict(market_data)
    market_data["news_risk"] = news_risk
    market_data["recent_history"] = summarize_recent()

    model = select_model(
        task="analysis",
        high_volatility=market_data.get("indicators", {}).get("volatility") == "HIGH",
    )
    market_data["_model_hint"] = model

    decision = analyze_market(market_data)

    if news_risk == "HIGH":
        decision["decision"] = "WAIT"
        decision["risk_warning"] = "High-impact news window active."

    decision = evaluate_risk(decision, market_data)

    record_decision(market_data, decision)
    return decision
