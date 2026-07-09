import requests

from config import (
TELEGRAM_TOKEN,
TELEGRAM_CHAT_ID
)


def send_message(message):

    if not TELEGRAM_TOKEN:
        print(message)
        return


    url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"


    requests.post(
        url,
        json={
        "chat_id":TELEGRAM_CHAT_ID,
        "text":message
        }
    )
