import httpx
import os

from time import time, sleep
from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel

from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

DOODSTREAM_API_KEY = '54845tb4kbkj7svvyig18'

TOKEN = '7379831394:AAEwRFQBAGJmqQOdD3g0BxErJCE-8uktczw'

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


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def handle_video(update, context):
    video = update.message.video
    file_id = video.file_id
    new_file = context.bot.get_file(file_id)
    file_path = new_file.file_path
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{file_path}")

def handle_message(update, context):
    message_text = update.message.text
    upload_to_filemoon(message_text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Message uploaded: {message_text}")

def upload_to_filemoon(message):
    url = "https://filemoonapi.com/api/remote/add"
    params = {
        "key": "54845tb4kbkj7svvyig18",  # replace with your actual API key
        "url": message
    }
     
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    print(response.json())
    if response.status_code == 200:
        print("Message uploaded successfully")
    else:
        print("Failed to upload message")

def register_handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    video_handler = MessageHandler(Filters.video, handle_video)
    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(video_handler)
    dispatcher.add_handler(message_handler)

@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    bot = Bot(token=TOKEN)
    update = Update.de_json(webhook_data.__dict__, bot) # convert the Telegram Webhook class to dictionary using __dict__ dunder method
    dispatcher = Dispatcher(bot, None, workers=4)
    register_handlers(dispatcher)

    # handle webhook request
    dispatcher.process_update(update)
      
    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}
