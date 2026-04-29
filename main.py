from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.get("/")
async def home():
    return {"status": "FXH signal bot running"}


@app.post("/webhook/mt5/signal")
async def receive_signal(request: Request):
    body = await request.body()
    print("RAW BODY:", body)

    if not body:
        return {"status": "error", "message": "Empty body"}

    try:
        data = json.loads(body)
    except Exception as e:
        print("JSON ERROR:", str(e))
        return {"status": "error", "message": "Invalid JSON"}

    print("JSON:", data)

    strategy = data.get("strategy", "N/A")
    symbol = data.get("symbol", "N/A")
    action = data.get("action", "N/A")
    entry = data.get("entry", "N/A")
    sl = data.get("sl", "N/A")
    tp = data.get("tp", "N/A")
    risk = data.get("risk", "N/A")
    lot = data.get("lot", "N/A")
    winrate = data.get("winrate", "N/A")

    text = f"""
📊 FXH SIGNAL

Strategy: {strategy}
Symbol: {symbol}
Action: {action}

Entry: {entry}
SL: {sl}
TP: {tp}

Risk: {risk}
Lot: {lot}
Winrate: {winrate}
"""

    if not BOT_TOKEN or not CHAT_ID:
        return {"status": "error", "message": "BOT_TOKEN or CHAT_ID missing"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    res = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    }, timeout=10)

    print("Telegram response:", res.text)

    return {
        "status": "sent",
        "telegram_status": res.status_code,
        "telegram_response": res.text
    }