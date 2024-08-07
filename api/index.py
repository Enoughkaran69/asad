import os
from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

TOKEN = os.environ.get("TOKEN")
FILEMOON_API_KEY = os.environ.get("FILEMOON_API_KEY")

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
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Video file path: {file_path}")

def handle_message(update, context):
    message = update.message
    if message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="File uploaded successfully!")
        


def register_handlers(dispatcher):
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text, handle_message)
    video_handler = MessageHandler(Filters.video, handle_video)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(video_handler)
    
@app.post("/webhook")
def webhook(webhook_data: TelegramWebhook):
    '''
    Telegram Webhook
    '''
    # Method 1
    bot = Bot(token=TOKEN)
    update = Update.de_json(webhook_data.__dict__, bot) # convert the Telegram Webhook class to dictionary using __dict__ dunder method
    dispatcher = Dispatcher(bot, None, workers=4)
    register_handlers(dispatcher)

    # handle webhook request
    dispatcher.process_update(update)
      

    # Method 2
    # you can just handle the webhook request here without using python-telegram-bot
    # if webhook_data.message:
    #     if webhook_data.message.text == '/start':
    #         send_message(webhook_data.message.chat.id, 'Hello World')

    return {"message": "ok"}

@app.get("/")
def index():
    return {"message": "Hello World"}
