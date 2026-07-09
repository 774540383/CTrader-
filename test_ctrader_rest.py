import os
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("CTRADER_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("CTRADER_ACCOUNT_ID")

print("===== cTrader REST Test =====")

print("ACCESS TOKEN:", "OK" if ACCESS_TOKEN else "MISSING")
print("ACCOUNT:", ACCOUNT_ID)

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://api.spotware.com/connect/tradingaccounts/{ACCOUNT_ID}"

try:
    r = requests.get(url, headers=headers)

    print("STATUS:", r.status_code)
    print(r.text[:1000])

except Exception as e:
    print("ERROR:", e)
