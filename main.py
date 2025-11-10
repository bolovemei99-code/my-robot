import os
import telebot
from flask import Flask, request

# 从环境变量读取 Token - 支持多个环境变量名
BOT_TOKEN = os.getenv('BOT_TOKEN') or os.getenv('TG_TOKEN')
if not BOT_TOKEN:
    raise ValueError('BOT_TOKEN or TG_TOKEN environment variable is required')

# 初始化机器人
bot = telebot.TeleBot(BOT_TOKEN)

# 创建 Flask 应用
app = Flask(__name__)

# Webhook 路由
@app.route('/webhook', methods=['POST'])
def webhook():
    """处理 Telegram Webhook 请求"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 400

@app.route('/setWebhook', methods=['GET'])
def set_webhook():
    """设置 Webhook"""
    webhook_url = os.getenv('RAILWAY_STATIC_URL') or os.getenv('RAILWAY_PUBLIC_DOMAIN')
    if webhook_url:
        if not webhook_url.startswith('http'):
            webhook_url = f'https://{webhook_url}'
        webhook_url = f'{webhook_url}/webhook'
        result = bot.set_webhook(url=webhook_url)
        if result:
            return f'Webhook set to {webhook_url}', 200
        else:
            return 'Failed to set webhook', 500
    return 'RAILWAY_STATIC_URL or RAILWAY_PUBLIC_DOMAIN not set', 400

@app.route('/', methods=['GET'])
def index():
    """主页"""
    return 'Telegram Bot is running!', 200

# Bot 命令处理
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """欢迎消息"""
    bot.reply_to(message, "你好！我是你的新机器人！发送 /help 查看帮助。")

@bot.message_handler(commands=['help'])
def send_help(message):
    """帮助信息"""
    help_text = """
🤖 可用命令：
/start - 开始使用
/help - 查看帮助
    """
    bot.reply_to(message, help_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """回显所有消息"""
    bot.reply_to(message, f"你说：{message.text}")

if __name__ == '__main__':
    # 获取端口
    port = int(os.getenv('PORT', 5000))
    
    # 如果有 Railway 域名，使用 webhook 模式
    if os.getenv('RAILWAY_STATIC_URL') or os.getenv('RAILWAY_PUBLIC_DOMAIN'):
        print(f"🚀 使用 Webhook 模式，端口：{port}")
        app.run(host='0.0.0.0', port=port)
    else:
        # 否则使用轮询模式
        print("🚀 使用轮询模式")
        bot.infinity_polling()
