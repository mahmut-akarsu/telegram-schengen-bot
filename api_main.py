import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = {
    "italya": int(os.getenv("ITALYA_CHAT_ID")),
    "fransa": int(os.getenv("FRANSA_CHAT_ID")),
    "bulgaristan": int(os.getenv("BULGARISTAN_CHAT_ID")),
    "hollanda":int(os.getenv("HOLLANDA_CHAT_ID")),
    "romanya":int(os.getenv("ROMANYA_CHAT_ID")),
    "yunanistan":int(os.getenv("YUNANISTAN_CHAT_ID"))
}

bot = Bot(BOT_TOKEN)
app = FastAPI()

class Message(BaseModel):
    text: str

@app.post("/{country}/announce")
async def announce(country: str, payload: Message):
    if country not in CHANNELS:
        raise HTTPException(status_code=404, detail="Bilinmeyen kanal")

    chat_id = CHANNELS[country]
    await bot.send_message(chat_id=chat_id, text=payload.text)

    return {
        "status": "sent",
        "channel": country,
        "chat_id": chat_id,
        "text": payload.text
    }

@app.get("/channels")
def list_channels():
    return CHANNELS
