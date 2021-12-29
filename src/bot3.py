from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random
import os
from dotenv import load_dotenv
load_dotenv()

def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

def mega(update: Update, context: CallbackContext) -> None:
    x = []
    for i in range(6):
        x.append(random.randint(1,60))
    update.message.reply_text(f'{update.effective_user.first_name} seu numero da sorte e \n {x}')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("""Bem Vido !\n/mega Verifique seu numero da sorte\n/hello Diga oi para o bot\nSelecione uma das opções acima para começar !""")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.effective_user.first_name}, vc esta pronto para começar')

token = os.getenv('MY_TOKEN')

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
<<<<<<< HEAD
updater.dispatcher.add_handler(CommandHandler('mega', mega))
=======
updater.dispatcher.add_handler(CommandHandler('meta', meta))
>>>>>>> 4e0b47c24d27375213d539e43ea9c574e5302e21
updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()