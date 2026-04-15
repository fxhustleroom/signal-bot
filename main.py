from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print("Telegram Error:", e)

@app.get("/")
def home():
    return {"status": "Bot is LIVE 🚀"}

@app.post("/webhook/mt5/signal")
async def receive_signal(req: Request):
    data = await req.json()

    symbol = data.get("symbol")
    action = data.get("action")
    entry = data.get("entry")
    sl = data.get("sl")
    tp = data.get("tp")

    message = f"""
📊 <b>FX SIGNAL</b>

Pair: {symbol}
Action: {action}
Entry: {entry}
SL: {sl}
TP: {tp}
"""

    send_telegram(message)

    return {"status": "sent"}