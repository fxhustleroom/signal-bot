from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# ✅ FIX CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.post("/webhook/mt5/signal")
async def receive_signal(request: Request):
    body = await request.body()
    print("RAW BODY:", body)

    if not body:
        return {"error": "Empty body"}

    data = await request.json()
    print("JSON:", data)

    text = f"""
📊 FXH SIGNAL

Symbol: {data.get('symbol')}
Action: {data.get('action')}
Entry: {data.get('entry')}
SL: {data.get('sl')}
TP: {data.get('tp')}
Risk: {data.get('risk')}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    res = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

    print("Telegram response:", res.text)

    return {"status": "sent"}