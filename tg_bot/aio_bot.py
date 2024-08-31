from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import load_config

config = load_config()
BOT_TOKEN = config.token.bot_token_srv

# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
answer = ''

@dp.message()
async def get_message(message: Message):
    await message.reply(text=f'Отправляю: {message.text}')
    global answer
    answer = message.text
    return answer


async def send_message(text: str):
    await bot.send_message(config.token.chat_id, text)




if __name__ == "__main__":
    dp.run_polling(bot)
    print(answer)

