from fastapi import FastAPI, Request
import requests
import os
import json

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.get("/")
async def home():
    return {"status": "running"}


@app.post("/webhook/mt5/signal")
async def receive_signal(request: Request):
    try:
        # 🔍 DEBUG: see raw incoming data
        body = await request.body()
        print("RAW BODY:", body)

        if not body:
            return {"error": "Empty body received"}

        # 🔍 Try parsing JSON safely
        try:
            data = json.loads(body)
        except Exception as e:
            print("JSON ERROR:", str(e))
            return {"error": "Invalid JSON"}

        print("PARSED JSON:", data)

        # ✅ Extract safely (no crash if missing)
        symbol = data.get("symbol", "N/A")
        action = data.get("action", "N/A")
        entry = data.get("entry", "N/A")
        sl = data.get("sl", "N/A")
        tp = data.get("tp", [])
        risk = data.get("risk", "N/A")

        # Format TP nicely
        tp_text = ", ".join([str(x) for x in tp]) if isinstance(tp, list) else str(tp)

        text = f"""
📊 *FXH SIGNAL*

Symbol: {symbol}
Action: {action}
Entry: {entry}
SL: {sl}
TP: {tp_text}

Risk: {risk}
"""

        # 🚀 Send to Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        response = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        })

        print("TELEGRAM RESPONSE:", response.text)

        return {"status": "sent"}

    except Exception as e:
        print("FATAL ERROR:", str(e))
        return {"error": str(e)}