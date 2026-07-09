from fastapi import FastAPI
from threading import Thread
import time

from ai.decision_engine import make_decision
from telegram.bot import send_message, start_command_listener
from ctrader.client import client
from ctrader.market_data import (
    get_latest_price,
    get_mid_price,
    subscribe_spots,
    subscribe_live_trendbars,
    request_historical_trendbars,
)
from ctrader.account import get_account_info, request_trader_info
from ctrader.symbols import get_symbol_id, request_symbols_list
from ctrader.positions import request_reconcile
from market.candles import get_dataframe
from market.indicators import add_indicators, latest_snapshot
from analysis.confluence import get_confluence
from execution.executor import execute_decision
from risk.daily_loss import set_starting_balance
from database.models import init_db
from database.history import save_decision, save_trade
from dashboard.api import router as dashboard_router
from logs.logger import get_logger
from config import SYMBOL, CTRADER_ACCOUNT_ID

logger = get_logger("main")

app = FastAPI()
app.include_router(dashboard_router)

running = True
_bootstrap_done = False


@app.get("/")
def home():
    return {
        "status": "cTrader AI Trading Bot Running",
        "symbol": SYMBOL,
        "ctrader_ready": client.ready,
    }


@app.get("/health")
def health():
    return {
        "alive": True,
        "ctrader_connected": client.connected,
        "ctrader_ready": client.ready,
    }


@app.get("/positions")
def positions():
    from ctrader.positions import get_open_positions
    return {"positions": get_open_positions()}


def _account_id() -> int:
    return int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0


def _bootstrap_ctrader() -> bool:
    """Wait for auth handshake, then request symbols/account/history and subscribe."""
    global _bootstrap_done

    if not client.wait_until_ready(timeout=25):
        logger.error("cTrader client did not become ready in time. Will keep retrying in background.")
        return False

    account_id = _account_id()

    request_trader_info(account_id)
    request_symbols_list(account_id)
    time.sleep(2)  # allow symbols list to populate before resolving symbol id

    symbol_id = get_symbol_id(SYMBOL)
    request_historical_trendbars(symbol_id, account_id, count=300, period="M5")
    subscribe_spots([symbol_id])
    subscribe_live_trendbars(symbol_id, period="M5")
    request_reconcile()

    account_info = get_account_info()
    set_starting_balance(account_info.get("balance") or 1000)

    _bootstrap_done = True
    send_message(f"✅ cTrader connected and authenticated. Bot is live-monitoring {SYMBOL}")
    logger.info("cTrader bootstrap complete.")
    return True


def trading_loop():
    send_message("🤖 cTrader AI Trading Bot Started")

    while running:
        try:
            if not _bootstrap_done:
                _bootstrap_ctrader()
                time.sleep(5)
                continue

            symbol_id = get_symbol_id(SYMBOL)
            df = get_dataframe(SYMBOL)

            if len(df) < 60:
                logger.info(f"Waiting for enough candles ({len(df)}/60) before analyzing.")
                time.sleep(20)
                continue

            df_ind = add_indicators(df)
            indicators = latest_snapshot(df_ind)
            confluence = get_confluence(df_ind, indicators)

            price = get_mid_price(symbol_id) or get_latest_price(symbol_id)

            market_data = {
                "symbol": SYMBOL,
                "price": price,
                "timeframe": "M5",
                "indicators": indicators,
                "confluence": confluence,
                "account_balance": get_account_info().get("balance") or 1000,
            }

            decision = make_decision(market_data)
            logger.info(f"Decision: {decision}")
            save_decision(decision, SYMBOL)

            if decision.get("decision") in ("BUY", "SELL"):
                result = execute_decision(decision, market_data, confluence)
                logger.info(f"Execution result: {result}")

                if result.get("executed"):
                    save_trade(
                        symbol=SYMBOL,
                        side=decision["decision"],
                        volume=decision.get("approved_position_size", 0.01),
                        entry_price=price,
                    )
                    send_message(
                        f"✅ {decision.get('decision')} {SYMBOL} executed\n"
                        f"Price: {price}\n"
                        f"Confidence: {decision.get('confidence')}\n"
                        f"Reason: {decision.get('entry_reason', '')}"
                    )
                else:
                    send_message(
                        f"⏸ Signal {decision.get('decision')} not executed: "
                        f"{result.get('reason')}"
                    )
            else:
                logger.info(f"No trade this cycle. Confidence={decision.get('confidence')}")

        except Exception as exc:
            logger.error(f"Trading loop error: {exc}")

        time.sleep(60)


@app.on_event("startup")
def on_startup():
    init_db()
    client.start()
    start_command_listener()


Thread(
    target=trading_loop,
    daemon=True,
).start()
