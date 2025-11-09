import telebot
import os
from datetime import datetime, timezone, timedelta
from flask import Flask, request

TOKEN = os.getenv('TG_TOKEN')
RAILWAY_URL = os.getenv('RAILWAY_STATIC_URL')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 自动回复规则
REPLIES = {
    "hi": lambda: f"你好！{get_current_time_utc7()}",
    "hello": "嗨！",
    "bye": "再见！",
    "帮助": "发 hi 试试自动回复"
}

def get_current_time_utc7():
    """获取当前 UTC+7 时间，格式为 HH:MM +07"""
    utc7 = timezone(timedelta(hours=7))
    now = datetime.now(utc7)
    return now.strftime("%H:%M +07")

@bot.message_handler(func=lambda msg: True)
def auto_reply(message):
    text = message.text.lower()
    for key, value in REPLIES.items():
        if key in text:
            reply_text = value() if callable(value) else value
            bot.reply_to(message, reply_text)
            return
    # 默认回复
    bot.reply_to(message, "我听到了！")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    """接收 Telegram webhook"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return '', 403

@app.route('/setWebhook', methods=['GET', 'POST'])
def set_webhook():
    """设置 Telegram webhook"""
    if RAILWAY_URL:
        webhook_url = f"https://{RAILWAY_URL}/{TOKEN}"
        result = bot.set_webhook(url=webhook_url)
        if result:
            return f"Webhook 设置成功！URL: {webhook_url}"
        else:
            return "Webhook 设置失败！"
    else:
        return "错误：RAILWAY_STATIC_URL 环境变量未设置"

@app.route('/')
def index():
    """首页，显示机器人状态"""
    return "Telegram 机器人正在运行！"

if __name__ == '__main__':
    print("Telegram 机器人已启动（Webhook 模式）！")
    # 开发环境下可以使用 set_webhook
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)