from ai.openrouter_client import analyze_market


market = {

    "symbol":"XAUUSD",

    "timeframe":"M5",

    "price":3350,

    "trend":"bullish",

    "indicators":{

        "EMA50":"above EMA200",

        "RSI":60,

        "MACD":"positive",

        "ATR":5

    },

    "market_structure":"higher highs",

    "supply_demand":"demand zone",

    "volume":"normal",

    "news":"no major news"

}


result = analyze_market(market)

print(result)
