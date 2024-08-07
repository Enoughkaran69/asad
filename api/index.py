import os
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging

TOKEN = os.environ.get("TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")


app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
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



@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await message.reply(f"File path: {file_path}")

@app.post("/webhook")
async def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    logger.info(f"Received webhook data: {webhook_data}")

    update = Update.de_json(webhook_data.__dict__, dp)
    
    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
