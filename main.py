from flask import Flask, request
import telebot
import sqlite3
import os
import json
import schedule
import time
from datetime import datetime
from threading import Thread
import requests

app = Flask(__name__)
TOKEN = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 数据库
db = sqlite3.connect('data.db', check_same_thread=False)
c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS accounts (user_id INTEGER, amount REAL, desc TEXT, time TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS quick (trigger TEXT PRIMARY KEY, response TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS messages (chat_id INTEGER, user_id INTEGER, msg_time TEXT)')
db.commit()

# 快捷回复
QUICK = {}
if os.path.exists('quick.json'):
    with open('quick.json', 'r', encoding='utf-8') as f:
        QUICK = json.load(f)

def save_quick():
    with open('quick.json', 'w', encoding='utf-8') as f:
        json.dump(QUICK, f, ensure_ascii=False)

# 管理员检查
def is_admin(chat_id, user_id):
    return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']

# 定时任务
def job_summary():
    c.execute("SELECT user_id, COUNT(*) FROM messages GROUP BY user_id")
    active = {uid: count for uid, count in c.fetchall()}
    bot.send_message(-1001234567890, f"📊 {datetime.now().strftime('%H:%M')} 总结:\n" + "\n".join([f"用户 {uid} 活跃 {count}" for uid, count in active.items()]))

def job_backup():
    with open(f'backup_{datetime.now().strftime("%H%M")}.db', 'wb') as f:
        f.write(sqlite3.serialize(db))
    bot.send_message(-1001234567890, "✅ 备份完成！")

def job_clean():
    c.execute("DELETE FROM messages WHERE julianday(msg_time) < julianday(?)", (datetime.now().strftime("%Y-%m-%d"),))
    db.commit()
    bot.send_message(-1001234567890, f"🧹 清理 {c.rowcount} 条！")

schedule.every().day.at("16:50").do(job_summary)
schedule.every().day.at("16:55").do(job_backup)
schedule.every().day.at("17:00").do(job_clean)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

Thread(target=run_schedule, daemon=True).start()

# Webhook 路由
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return '', 200

# 自动回复
@bot.message_handler(content_types=['text'])
def auto_reply(message):
    c.execute("INSERT INTO messages VALUES (?, ?, ?)", (message.chat.id, message.from_user.id, datetime.now().strftime("%Y-%m-%d %H:%M")))
    db.commit()
    text = message.text.lower()
    user_id = message.from_user.id
    if 'hi' in text: return bot.reply_to(message, f"你好！{datetime.now().strftime('%H:%M')} +07。")
    if '天气' in text: return bot.reply_to(message, "晴，17°C（模拟）。")
    if trigger := next((k for k in QUICK if k in text), None):
        return bot.reply_to(message, QUICK[trigger])
    bot.reply_to(message, "/help 查看命令！")

# AI 对话
@bot.message_handler(commands=['ai'])
def ai_dialog(message):
    query = ' '.join(message.text.split()[1:]) or "你好"
    api_key = os.getenv('XAI_API_KEY')
    if not api_key:
        bot.reply_to(message, "❌ 未配置 xAI API Key！")
        return
    url = "https://api.x.ai/v1/chat"  # 假设 xAI API 端点
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"message": query, "user_id": str(message.from_user.id)}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=5)
        if response.status_code == 200:
            reply = response.json().get("response", "AI 处理中...")
            bot.reply_to(message, f"🤖 AI: {reply}")
        else:
            bot.reply_to(message, f"❌ AI 错误: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"❌ AI 请求失败: {str(e)}")

# 群组管理
@bot.message_handler(commands=['kick', 'ban'], chat_types=['supergroup'])
def manage_group(message):
    if not is_admin(message.chat.id, message.from_user.id): return bot.reply_to(message, "❌ 仅限管理员！")
    try:
        target_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.text.split()[1])
        if message.text.startswith('/kick'):
            bot.kick_chat_member(message.chat.id, target_id)
            bot.unban_chat_member(message.chat.id, target_id)
            return bot.reply_to(message, f"✅ 踢出 {target_id}")
        if message.text.startswith('/ban'):
            bot.kick_chat_member(message.chat.id, target_id)
            return bot.reply_to(message, f"✅ 封禁 {target_id}")
    except: bot.reply_to(message, "❌ 失败！")

# 硬件控制（模拟）
@bot.message_handler(commands=['hw'])
def hw_control(message):
    if not is_admin(message.chat.id, message.from_user.id): return bot.reply_to(message, "❌ 仅限管理员！")
    cmd = message.text.split()[1].lower() if len(message.text.split()) > 1 else ''
    response = {"on": "✅ 硬件开", "off": "✅ 硬件关"}.get(cmd, "❌ 无效命令")
    bot.reply_to(message, response)

# 记账
@bot.message_handler(commands=['add', 'sub', 'balance'])
def account_cmd(message):
    cmd = message.text.split()[0][1:]
    try:
        if cmd == 'balance':
            c.execute("SELECT SUM(amount) FROM accounts WHERE user_id=?", (message.from_user.id,))
            total = c.fetchone()[0] or 0
            return bot.reply_to(message, f"💰 余额: {total}")
        amount = float(message.text.split()[1])
        desc = ' '.join(message.text.split()[2:]) or '无描述'
        c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)",
                  (message.from_user.id, amount if cmd == 'add' else -amount, desc, datetime.now().strftime("%m-%d %H:%M")))
        db.commit()
        bot.reply_to(message, f"✅ {amount if cmd == 'add' else -amount} | {desc}")
    except: bot.reply_to(message, f"❌ 格式: /{cmd} 10 描述")

# 快捷回复
@bot.message_handler(commands=['setquick', 'getquick'])
def quick_cmd(message):
    cmd = message.text.split()[0][1:]
    try:
        if cmd == 'getquick':
            return bot.reply_to(message, f"📋 快捷: {', '.join(f'{k}→{v}' for k, v in QUICK.items()) or '无'}")
        trigger, response = message.text.split(maxsplit=2)[1].lower(), message.text.split(maxsplit=2)[2]
        QUICK[trigger] = response
        save_quick()
        bot.reply_to(message, f"✅ {trigger} → {response}")
    except: bot.reply_to(message, f"❌ 格式: /{cmd} hi 你好")

# 群发
@bot.message_handler(commands=['mass'])
def mass_cmd(message):
    if message.chat.type != 'private' or not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ 私聊管理员专用！")
    try:
        targets, msg = message.text.split(maxsplit=1)[1].split(), "群发消息"
        if len(message.text.split()) > 2: msg = ' '.join(message.text.split()[2:])
        success = sum(1 for t in targets if bot.send_message(int(t), msg))
        bot.reply_to(message, f"📬 完成: {success}/{len(targets)}")
    except: bot.reply_to(message, "❌ 格式: /mass 123 456 消息")

# 帮助
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "🎉 命令: /add 10 午饭 /sub 5 咖啡 /balance /setquick hi 你好 /getquick /mass 123 消息 /kick /ban /ai /hw on/off /help")

# 启动 Webhook
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.getenv('VERCEL_URL')}/webhook")
    print(f"Webhook set at {datetime.now().strftime('%H:%M')} +07")