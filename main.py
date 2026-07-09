from fastapi import FastAPI
from threading import Thread
import time

from ai.decision_engine import make_decision
from telegram.bot import send_message, start_command_listener
from ctrader.client import client
from ctrader.market_data import get_latest_price, subscribe_spots
from market.candles import add_candle, get_dataframe
from market.indicators import add_indicators, latest_snapshot
from database.models import init_db
from config import SYMBOL

app = FastAPI()

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

            if len(df) >= 50:
                df = add_indicators(df)
                indicators = latest_snapshot(df)
            else:
                indicators = {"RSI": 50, "EMA50": "", "EMA200": ""}

            market_data = {
                "symbol": SYMBOL,
                "price": get_latest_price(1),
                "timeframe": "M5",
                "indicators": indicators,
            }

            decision = make_decision(market_data)
            print(decision)

            if decision.get("decision") in ("BUY", "SELL"):
                send_message(
                    f"Signal: {decision.get('decision')} {SYMBOL} "
                    f"(confidence={decision.get('confidence')})\n"
                    f"Reason: {decision.get('entry_reason', '')}"
                )

        except Exception as exc:
            print("Trading loop error:", exc)

        time.sleep(60)


@app.on_event("startup")
def on_startup():
    init_db()
    client.start()
    subscribe_spots([1])
    start_command_listener()


Thread(
    target=trading_loop,
    daemon=True,
).start()
