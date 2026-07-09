# ai/openrouter_client.py

import requests
import json

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def analyze_market(market_data):

    if not OPENROUTER_API_KEY:
        return {
            "decision": "WAIT",
            "confidence": 0,
            "error": "Missing OpenRouter API Key"
        }


    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost",
        "X-Title": "Gold AI Trading Agent"
    }


    system_prompt = """
You are an advanced XAUUSD gold trading analyst.

Analyze the provided market data.

Rules:
- Protect capital.
- Do not force trades.
- Return ONLY JSON.
- No markdown.
- No explanation outside JSON.

Required JSON format:

{
"decision":"BUY/SELL/WAIT",
"confidence":0,
"entry_reason":"",
"market_condition":"",
"stop_loss_logic":"",
"take_profit_logic":"",
"trade_duration":"",
"risk_warning":""
}

Decision rules:
- confidence below 85 = WAIT
- Never trade without confirmation.
"""


    payload = {

        "model": OPENROUTER_MODEL,

        "messages": [

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": json.dumps(
                    market_data,
                    ensure_ascii=False
                )
            }

        ],

        "temperature": 0.1,

        "max_tokens": 800

    }


    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )


        result = response.json()


        # معالجة أخطاء OpenRouter
        if "choices" not in result:

            print("\n========== OPENROUTER ERROR ==========")
            print(json.dumps(result, indent=2))
            print("======================================\n")

            return {
                "decision": "WAIT",
                "confidence": 0,
                "error": result
            }


        content = result["choices"][0]["message"]["content"]


        # تنظيف الرد
        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()


        try:

            ai_result = json.loads(content)

        except Exception:

            ai_result = {

                "decision": "WAIT",

                "confidence": 0,

                "error": "Invalid JSON from AI",

                "raw_response": content

            }


        return ai_result



    except requests.exceptions.Timeout:

        return {

            "decision": "WAIT",

            "confidence": 0,

            "error": "OpenRouter timeout"

        }



    except Exception as e:

        return {

            "decision": "WAIT",

            "confidence": 0,

            "error": str(e)

        }
