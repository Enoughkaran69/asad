import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from telethon import TelegramClient, events
import logging

TOKEN = os.environ.get("TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
client = TelegramClient('in_memory_session_name', API_ID, API_HASH).start(bot_token=TOKEN)

app = FastAPI()
# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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



@client.on(events.NewMessage)
async def handler(event):
    if event.message.file:
        file_id = event.message.file.id
        file = await client.get_messages(event.message.chat_id, ids=file_id)
        file_path = file.file.name
        await event.reply(f"File path: {file_path}")

@app.post("/webhook")
async def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    logger.info(f"Received webhook data: {webhook_data}")

    update = Update.de_json(webhook_data.__dict__, client)
    
    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}

client.run_until_disconnected()
