from fastapi import FastAPI
from threading import Thread
import time

from ai.decision_engine import make_decision
from telegram.bot import send_message, start_command_listener
from ctrader.client import client
from ctrader.market_data import get_latest_price, subscribe_spots
from ctrader.account import get_account_info, request_trader_info
from ctrader.symbols import get_symbol_id, request_symbols_list
from market.candles import add_candle, get_dataframe
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


@app.get("/")
def home():
    return {
        "status": "cTrader AI Trading Bot Running",
        "symbol": SYMBOL,
    }


@app.get("/health")
def health():
    return {
        "alive": True,
        "ctrader_connected": client.connected,
    }


@app.get("/positions")
def positions():
    from ctrader.positions import get_open_positions
    return {"positions": get_open_positions()}


def trading_loop():
    send_message("🤖 cTrader AI Trading Bot Started")

    while running:
        try:
            df = get_dataframe(SYMBOL)

            if len(df) >= 200:
                df_ind = add_indicators(df)
                indicators = latest_snapshot(df_ind)
                confluence = get_confluence(df_ind, indicators)
            else:
                df_ind = df
                indicators = {"RSI": 50, "EMA50": "", "EMA200": ""}
                confluence = {"confluence_score": 0, "trend": "UNKNOWN"}

            market_data = {
                "symbol": SYMBOL,
                "price": get_latest_price(get_symbol_id(SYMBOL)),
                "timeframe": "M5",
                "indicators": indicators,
                "confluence": confluence,
                "account_balance": get_account_info().get("balance", 1000),
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
                    )
                    send_message(
                        f"✅ {decision.get('decision')} {SYMBOL} executed\n"
                        f"Confidence: {decision.get('confidence')}\n"
                        f"Reason: {decision.get('entry_reason', '')}"
                    )
                else:
                    send_message(
                        f"⏸ Signal {decision.get('decision')} not executed: "
                        f"{result.get('reason')}"
                    )

        except Exception as exc:
            logger.error(f"Trading loop error: {exc}")

        time.sleep(60)


@app.on_event("startup")
def on_startup():
    init_db()
    client.start()

    account_id = int(CTRADER_ACCOUNT_ID) if CTRADER_ACCOUNT_ID else 0
    time.sleep(2)  # allow WS auth to complete before requesting data
    request_trader_info(account_id)
    request_symbols_list(account_id)
    subscribe_spots([get_symbol_id(SYMBOL)])

    account_info = get_account_info()
    set_starting_balance(account_info.get("balance", 1000))

    start_command_listener()


Thread(
    target=trading_loop,
    daemon=True,
).start()
