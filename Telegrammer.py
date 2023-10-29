# Steps to install telebot package:
# 1. Open terminal
# 2. Type: pip install pyTelegramBotAPI

import telebot
from datetime import datetime as dt

class Telegrammer:
    def __init__(self, token='5817388358:AAFjBOYrJMw-mPsR7upUIyZtcIr3loEGn2Y'):
        self.tb = telebot.TeleBot(token)
        # self.chat_id = self.tb.get_me().id

        @self.tb.message_handler(commands=['start']) 
        def sendWelcome(message): 
            self.tb.send_message(message.chat.id, f"Welcome to the Music Player Bot. Type /help to see the list of commands.")

        @self.tb.message_handler(commands=['register']) 
        def registerMe(message):
            self.tb.reply_to(message, f"Wait, registering you...")
            self.tb.reply_to(message, f"Alright, you have been registered.")

        self.tb.infinity_polling(30)


    def sendMessage(self, message):
        self.tb.send_message('370235141', message)
