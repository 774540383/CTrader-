"""
telegram/bot.py
Telegram integration: outbound alerts (existing behaviour preserved) plus
inbound command handling for status/positions/history queries.
"""
import requests
import threading
import time

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}" if TELEGRAM_TOKEN else None
_last_update_id = 0


def send_message(message: str):
    if not TELEGRAM_TOKEN:
        print(message)
        return

    url = f"{BASE_URL}/sendMessage"
    try:
        requests.post(
            url,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": message},
            timeout=15,
        )
    except Exception as exc:
        print("Telegram send_message error:", exc)


def _handle_command(text: str) -> str:
    text = text.strip().lower()
    from telegram.commands import cmd_status, cmd_history, cmd_help

    if text in ("/status", "status"):
        return cmd_status()

    if text in ("/positions", "positions"):
        from ctrader.positions import get_open_positions
        positions = get_open_positions()
        if not positions:
            return "No open positions."
        return "\n".join(str(p) for p in positions)

    if text in ("/history", "history"):
        return cmd_history()

    if text in ("/help", "help"):
        return cmd_help()

    return None


def _poll_updates():
    global _last_update_id
    if not BASE_URL:
        return

    while True:
        try:
            resp = requests.get(
                f"{BASE_URL}/getUpdates",
                params={"offset": _last_update_id + 1, "timeout": 30},
                timeout=40,
            )
            data = resp.json()
            for update in data.get("result", []):
                _last_update_id = update["update_id"]
                message = update.get("message", {})
                text = message.get("text", "")
                chat_id = message.get("chat", {}).get("id")

                reply = _handle_command(text)
                if reply and chat_id:
                    requests.post(
                        f"{BASE_URL}/sendMessage",
                        json={"chat_id": chat_id, "text": reply},
                        timeout=15,
                    )
        except Exception as exc:
            print("Telegram polling error:", exc)
            time.sleep(5)


def start_command_listener():
    """Start polling for inbound Telegram commands on a background thread."""
    if not TELEGRAM_TOKEN:
        return
    thread = threading.Thread(target=_poll_updates, daemon=True)
    thread.start()
