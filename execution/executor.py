"""
execution/executor.py
Execution Engine: orchestrates validation, strategy choice, and order
placement, then hands the resulting position to risk management for
ongoing trailing stop / breakeven management.
"""
from execution.validator import validate_trade
from execution.strategy import choose_entry_strategy
from ctrader.orders import send_market_order
from risk.daily_loss import get_daily_loss_percent
from logs.logger import get_logger

logger = get_logger("execution.executor")

SYMBOL_ID_MAP = {"XAUUSD": 1}


def execute_decision(decision: dict, market_data: dict, confluence: dict) -> dict:
    is_valid, reason = validate_trade(decision, market_data)
    if not is_valid:
        logger.info(f"Trade rejected: {reason}")
        return {"executed": False, "reason": reason}

    if get_daily_loss_percent() >= 5.0:
        logger.warning("Daily loss limit reached, blocking new trade.")
        return {"executed": False, "reason": "Daily loss limit reached."}

    entry_type = choose_entry_strategy(decision, confluence)
    if entry_type == "NO_ENTRY":
        return {"executed": False, "reason": "Strategy declined entry."}

    symbol = market_data.get("symbol", "XAUUSD")
    symbol_id = SYMBOL_ID_MAP.get(symbol, 1)
    volume = decision.get("approved_position_size", 0.01)

    result = send_market_order(
        symbol_id=symbol_id,
        volume=int(volume * 100),
        side=decision["decision"],
    )
    logger.info(f"Trade executed: {result}")
    return {"executed": True, "order_result": result, "entry_type": entry_type}
