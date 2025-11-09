import telebot
import os
from flask import Flask, request

TOKEN = os.getenv('TG_TOKEN')
WEBHOOK_URL = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return '', 403

@app.route('/setWebhook', methods=['GET'])
def set_webhook():
    webhook_url = f"https://{WEBHOOK_URL}/{TOKEN}"
    result = bot.set_webhook(url=webhook_url)
    if result:
        return f"Webhook set to {webhook_url}", 200
    else:
        return "Failed to set webhook", 500

@app.route('/')
def index():
    return "Telegram Bot is running!", 200

if __name__ == '__main__':
    print("Telegram 机器人已启动！")
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)