from fastapi import FastAPI
from threading import Thread
import time


from ai.openrouter_client import analyze_market
from telegram.bot import send_message


app=FastAPI()


running=True



@app.get("/")
def home():

    return {
    "status":"Gold AI Trading Bot Running"
    }



@app.get("/health")
def health():

    return {
    "alive":True
    }



def trading_loop():

    send_message(
    "🤖 Gold AI Trading Bot Started"
    )


    while running:


        market_data={

        "symbol":"XAUUSD",

        "price":"TEST",

        "timeframe":"M5",

        "indicators":{

        "RSI":50,

        "EMA50":"",

        "EMA200":""

        }

        }



        decision=analyze_market(
            market_data
        )


        print(decision)



        time.sleep(60)




Thread(
target=trading_loop,
daemon=True
).start()
