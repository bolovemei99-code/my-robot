import telebot
import os
from datetime import datetime

TOKEN = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 自动回复规则
REPLIES = {
    "hi": "你好！",
    "hello": "嗨！",
    "bye": "再见！",
    "帮助": "发 hi 试试自动回复"
}

@bot.message_handler(func=lambda msg: True)
def auto_reply(message):
    text = message.text.lower()
    for key, value in REPLIES.items():
        if key in text:
            bot.reply_to(message, value)
            return
    # 默认回复
    bot.reply_to(message, "我听到了！")

print("Telegram 机器人已启动！")
bot.polling()