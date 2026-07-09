import os
import requests
from dotenv import load_dotenv

load_dotenv()


print("\n===== Gold AI Trading Bot Connection Test =====\n")


# OpenRouter

api_key = os.getenv("OPENROUTER_API_KEY")

if api_key:
    print("✅ OpenRouter API Key: OK")
else:
    print("❌ OpenRouter API Key: Missing")



# Telegram

telegram_token = os.getenv("TELEGRAM_TOKEN")
telegram_chat = os.getenv("TELEGRAM_CHAT_ID")


if telegram_token and telegram_chat:

    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

    data = {
        "chat_id": telegram_chat,
        "text": "🤖 Gold AI Trading Bot Test Message"
    }

    try:
        r = requests.post(url, data=data, timeout=10)

        if r.status_code == 200:
            print("✅ Telegram: OK")
        else:
            print("❌ Telegram Error:")
            print(r.text)

    except Exception as e:
        print("❌ Telegram Connection Error")
        print(e)

else:
    print("⚠️ Telegram keys not added yet")



# cTrader

client_id = os.getenv("CTRADER_CLIENT_ID")
secret = os.getenv("CTRADER_SECRET")
account = os.getenv("CTRADER_ACCOUNT_ID")
token = os.getenv("CTRADER_ACCESS_TOKEN")


if client_id and secret and account and token:

    print("✅ cTrader Credentials: FOUND")

else:

    print("⚠️ cTrader Credentials: Missing")



print("\n===== Test Finished =====")
