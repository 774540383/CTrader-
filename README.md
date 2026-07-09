# cTrader AI Trading Agent

Production-oriented AI trading system for TopFX cTrader (XAUUSD focus),
built with FastAPI, OpenRouter, Telegram, and the cTrader Open API.

## Architecture

- **FastAPI** app (`main.py`) exposes `/`, `/health`, and `/positions`, and
  runs the trading loop in a background thread. Deployed on Render via
  Docker/Procfile/start.sh (all unchanged).
- **ctrader/** — Open API integration: OAuth2 auth (`auth.py`), outbound
  WebSocket client (`client.py`), live spot cache (`market_data.py`),
  order execution (`orders.py`), and position tracking (`positions.py`).
- **ai/** — AI Decision Engine: OpenRouter client, model selector, rolling
  decision memory, and the main `decision_engine.py` pipeline.
- **risk/** — Smart Risk Manager: position sizing, cooldown/daily-loss
  protection, and the final trade gatekeeper.
- **market/** — Candle buffer, technical indicators, price action, market
  structure, and supply/demand zones.
- **analysis/** — Higher-level trend, volatility, liquidity, and confluence
  scoring built on top of `market/`.
- **news/** — Economic calendar fetch and a news-risk filter that forces
  `WAIT` around high-impact USD news.
- **database/** — SQLAlchemy models, SQLite by default, switch to
  PostgreSQL by only changing `DATABASE_URL`.
- **telegram/** — Outbound alerts plus inbound `/status`, `/positions`,
  `/help` commands.
- **tests/** — Unit tests for risk sizing and confluence scoring.

## Environment variables

See `.env.example`. Configured on Render as `sync: false` secrets in
`render.yaml`: `OPENROUTER_API_KEY`, `CTRADER_CLIENT_ID`, `CTRADER_SECRET`,
`CTRADER_ACCESS_TOKEN`, `CTRADER_REFRESH_TOKEN`, `CTRADER_ACCOUNT_ID`,
`TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`. Optional: `DATABASE_URL`,
`PAPER_TRADING`, `SYMBOL`, `RISK_PERCENT`, `MAX_POSITIONS`,
`CTRADER_USE_LIVE`.

## Running locally

```
pip install -r requirements.txt
uvicorn main:app --reload
```

## Running tests

```
pytest tests/
```

## Deployment

No changes were made to `Dockerfile`, `Procfile`, `start.sh`, or the
`render.yaml` start command. Push to `main` and Render will redeploy
automatically.
