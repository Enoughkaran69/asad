import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from pyrogram import Client, filters
from pyrogram.types import Update

TOKEN = os.environ.get("TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

app = FastAPI()

class TelegramWebhook(BaseModel):
    '''
    Telegram Webhook Model using Pydantic for request body validation
    '''
    update_id: int
    message: Optional[dict]
    edited_message: Optional[dict]
    channel_post: Optional[dict]
    edited_channel_post: Optional[dict]
    inline_query: Optional[dict]
    chosen_inline_result: Optional[dict]
    callback_query: Optional[dict]
    shipping_query: Optional[dict]
    pre_checkout_query: Optional[dict]
    poll: Optional[dict]
    poll_answer: Optional[dict]

client = Client("ja69du_bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

@app.post("/webhook")
async def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    update = Update.de_json(webhook_data.__dict__, client)
    
    if update.message and update.message.video:
        video = update.message.video
        file_id = video.file_id
        file = await client.get_file(file_id)
        file_path = file.file_path
        await client.send_message(chat_id=update.message.chat.id, text=f"Video file path: {file_path}")
    
    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}

if __name__ == "__main__":
    client.run()
