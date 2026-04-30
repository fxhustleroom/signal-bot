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

    # ✅ FIX MT5 NULL BYTE ISSUE
    clean_body = body.replace(b"\x00", b"").strip()

    try:
        data = json.loads(clean_body.decode("utf-8"))
    except Exception as e:
        print("JSON ERROR:", str(e))
        return {"status": "error", "message": "Invalid JSON"}

    print("JSON:", data)

    text = f"""
📊 FXH SIGNAL

Strategy: {data.get("strategy", "N/A")}
Symbol: {data.get("symbol", "N/A")}
Action: {data.get("action", "N/A")}

Entry: {data.get("entry", "N/A")}
SL: {data.get("sl", "N/A")}
TP: {data.get("tp", "N/A")}

Risk: {data.get("risk", "N/A")}
Lot: {data.get("lot", "N/A")}
Winrate: {data.get("winrate", "N/A")}
Reason: {data.get("reason", "N/A")}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    res = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    }, timeout=10)

    print("Telegram response:", res.text)

    return {
        "status": "sent",
        "telegram_status": res.status_code
    }