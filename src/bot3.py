from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os
from dotenv import load_dotenv
load_dotenv()

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

def meta(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.effective_user.first_name} este é um teste de resposta')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.effective_user.first_name}, vc esta pronto para começar')

token = os.getenv('MY_TOKEN')

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('meta', meta))
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()