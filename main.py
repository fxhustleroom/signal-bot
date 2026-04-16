from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.post("/webhook/mt5/signal")
async def receive_signal(request: Request):
    body = await request.body()
    print("RAW BODY:", body)

    data = await request.json()
    print("JSON:", data)

    text = f"""
📊 *FXH SIGNAL*

Symbol: {data['symbol']}
Action: {data['action']}
Entry: {data['entry']}
SL: {data['sl']}
TP: {data['tp']}

Risk: {data['risk']}
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })

    return {"status": "sent"}