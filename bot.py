import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# 从环境变量读取 Token
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN 环境变量未设置！请在 Railway 中配置 BOT_TOKEN 环境变量。")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("你好！我是你的新机器人！")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    print("机器人正在启动...")
    executor.start_polling(dp, skip_updates=True)