from config import load_config

import telebot


config = load_config()
bot = telebot.TeleBot(token=config.token.bot_token_srv)
answer = ''

def bot_send_message(text):
    bot.send_message(chat_id=config.token.chat_id, text=text)



@bot.message_handler(content_types=['text'])  #Создаём новую функцию ,реагирующую на любое сообщение
def bot_answer(message):
    global answer  #объявляем глобальную переменную
    answer = message.text
    bot.reply_to(message, f'Ваш ответ: {message.text}')


if __name__ == '__main__':
    print(answer)
    bot.polling(none_stop=True)
    print(answer)
