import os
from dotenv import load_dotenv

load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "anthropic/claude-sonnet-4.5"
)


CTRADER_CLIENT_ID = os.getenv("CTRADER_CLIENT_ID")
CTRADER_SECRET = os.getenv("CTRADER_SECRET")
CTRADER_ACCOUNT_ID = os.getenv("CTRADER_ACCOUNT_ID")
CTRADER_ACCESS_TOKEN = os.getenv("CTRADER_ACCESS_TOKEN")
CTRADER_REFRESH_TOKEN = os.getenv("CTRADER_REFRESH_TOKEN")
CTRADER_USE_LIVE = (os.getenv("CTRADER_USE_LIVE", "false").lower() == "true")


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


PAPER_TRADING = (
    os.getenv("PAPER_TRADING", "true").lower() == "true"
)


SYMBOL = os.getenv(
    "SYMBOL",
    "XAUUSD"
)


RISK_PERCENT = float(
    os.getenv("RISK_PERCENT", 1)
)


MAX_POSITIONS = int(
    os.getenv("MAX_POSITIONS", 3)
)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ctrader.db")
