from config import load_config

import telebot


def bot_send_message(text):
    config = load_config()
    bot = telebot.TeleBot(token=config.token.bot_token_srv)
    bot.send_message(chat_id=config.token.chat_id, text=text)
