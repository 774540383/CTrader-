import os
import requests
from dotenv import load_dotenv

load_dotenv()


CLIENT_ID = os.getenv("CTRADER_CLIENT_ID")
ACCESS_TOKEN = os.getenv("CTRADER_ACCESS_TOKEN")
ACCOUNT_ID = os.getenv("CTRADER_ACCOUNT_ID")


print("===== cTrader Open API Test =====")

print("Client ID:", "OK" if CLIENT_ID else "MISSING")
print("Access Token:", "OK" if ACCESS_TOKEN else "MISSING")
print("Account ID:", ACCOUNT_ID)


if not ACCESS_TOKEN:
    print("Missing Access Token")
    exit()


headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}


# cTrader Open API account endpoint
url = (
    f"https://api.spotware.com/connect/tradingaccounts"
)


try:

    r = requests.get(
        url,
        headers=headers,
        timeout=10
    )


    print("\nStatus:", r.status_code)

    print(r.text[:1000])


except Exception as e:

    print("ERROR:")
    print(e)
