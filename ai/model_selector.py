"""
ai/model_selector.py
Chooses which OpenRouter model to use depending on task complexity and cost.
"""
from config import OPENROUTER_MODEL

FAST_MODEL = "anthropic/claude-3-haiku"
DEEP_MODEL = OPENROUTER_MODEL or "anthropic/claude-sonnet-4.5"


def select_model(task: str = "analysis", high_volatility: bool = False) -> str:
    """Pick a model based on the task type and current market conditions."""
    if task == "quick_check" and not high_volatility:
        return FAST_MODEL
    return DEEP_MODEL
