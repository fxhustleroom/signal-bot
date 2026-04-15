from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SECRET = os.getenv("SECRET")

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    if data.get("secret") != SECRET:
        return {"error": "unauthorized"}

    msg = f"""
📊 FX SIGNAL

Pair: {data['symbol']}
Type: {data['action']}

Entry: {data['entry']}
SL: {data['sl']}
TP: {data['tp']}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })

    return {"status": "sent"}