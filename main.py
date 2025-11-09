from flask import Flask, request
import telebot
import os
import sqlite3
import re
from datetime import datetime

app = Flask(__name__)
TOKEN = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 数据库
db = sqlite3.connect('data.db', check_same_thread=False)
c = db.cursor()
c.execute('CREATE TABLE IF NOT EXISTS accounts (user_id INTEGER, amount REAL, desc TEXT, time TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS quick (trigger TEXT PRIMARY KEY, response TEXT)')
db.commit()

# 快捷回复
QUICK = {}
if os.path.exists('quick.json'):
    with open('quick.json', 'r', encoding='utf-8') as f:
        QUICK = eval(f.read())

def save_quick():
    with open('quick.json', 'w', encoding='utf-8') as f:
        f.write(str(QUICK))

# 管理员检查
def is_admin(chat_id, user_id):
    try:
        return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']
    except:
        return False

# Webhook 路由
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return '', 200

# 自动回复
@bot.message_handler(content_types=['text'])
def auto_reply(message):
    text = message.text.lower()
    user_id = message.from_user.id
    # 正则匹配金额格式（如 10.5 或 10）
    if match := re.match(r'^\d+(\.\d+)?$', text):
        amount = float(match.group())
        c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (user_id, amount, '自动记账', datetime.now().strftime("%m-%d %H:%M")))
        db.commit()
        bot.reply_to(message, f"✅ 自动记 {amount} | {datetime.now().strftime('%H:%M')} +07")
    # 快捷回复
    elif trigger := next((k for k in QUICK if k in text), None):
        bot.reply_to(message, QUICK[trigger])
    else:
        bot.reply_to(message, "发送 /help 或金额试试！")

# 群管理
@bot.message_handler(commands=['kick', 'ban'], chat_types=['supergroup'])
def manage_group(message):
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ 仅限管理员！")
    try:
        target_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.text.split()[1])
        if message.text.startswith('/kick'):
            bot.kick_chat_member(message.chat.id, target_id)
            bot.unban_chat_member(message.chat.id, target_id)
            bot.reply_to(message, f"✅ 踢出 {target_id}")
        elif message.text.startswith('/ban'):
            bot.kick_chat_member(message.chat.id, target_id)
            bot.reply_to(message, f"✅ 封禁 {target_id}")
    except:
        bot.reply_to(message, "❌ 失败！")

# 群发（仅限管理员）
@bot.message_handler(commands=['mass'])
def mass_cmd(message):
    if message.chat.type != 'private' or not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ 私聊管理员专用！")
    try:
        targets, msg = message.text.split(maxsplit=1)[1].split(), "群发消息"
        if len(message.text.split()) > 2: msg = ' '.join(message.text.split()[2:])
        success = sum(1 for t in targets if bot.send_message(int(t), msg))
        bot.reply_to(message, f"📬 完成: {success}/{len(targets)}")
    except:
        bot.reply_to(message, "❌ 格式: /mass 123 456 消息")

# 记账
@bot.message_handler(commands=['add', 'sub', 'balance'])
def account_cmd(message):
    cmd = message.text.split()[0][1:]
    try:
        if cmd == 'balance':
            c.execute("SELECT SUM(amount) FROM accounts WHERE user_id=?", (message.from_user.id,))
            total = c.fetchone()[0] or 0
            bot.reply_to(message, f"💰 余额: {total}")
        else:
            amount = float(message.text.split()[1])
            desc = ' '.join(message.text.split()[2:]) or '无描述'
            c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)",
                      (message.from_user.id, amount if cmd == 'add' else -amount, desc, datetime.now().strftime("%m-%d %H:%M")))
            db.commit()
            bot.reply_to(message, f"✅ {amount if cmd == 'add' else -amount} | {desc}")
    except:
        bot.reply_to(message, f"❌ 格式: /{cmd} 10 描述")

# 快捷回复
@bot.message_handler(commands=['setquick', 'getquick'])
def quick_cmd(message):
    cmd = message.text.split()[0][1:]
    try:
        if cmd == 'getquick':
            bot.reply_to(message, f"📋 快捷: {', '.join(f'{k}→{v}' for k, v in QUICK.items()) or '无'}")
        else:
            trigger, response = message.text.split(maxsplit=2)[1].lower(), message.text.split(maxsplit=2)[2]
            QUICK[trigger] = response
            save_quick()
            bot.reply_to(message, f"✅ {trigger} → {response}")
    except:
        bot.reply_to(message, f"❌ 格式: /{cmd} hi 你好")

# 回复模板
@bot.message_handler(commands=['template'])
def set_template(message):
    try:
        template = ' '.join(message.text.split()[1:])
        if not template: return bot.reply_to(message, "❌ 请输入模板，如 /template 欢迎 {name}")
        QUICK['template'] = template
        save_quick()
        bot.reply_to(message, f"✅ 模板设为: {template}")
    except:
        bot.reply_to(message, "❌ 格式: /template 文本")

@bot.message_handler(content_types=['new_chat_members'])
def apply_template(message):
    for user in message.new_chat_members:
        if 'template' in QUICK:
            reply = QUICK['template'].replace('{name}', user.first_name)
            bot.reply_to(message, f"🎉 {reply}，{datetime.now().strftime('%H:%M')} +07")

# 帮助
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "🎉 命令: /add 10 午饭 /sub 5 咖啡 /balance /setquick hi 你好 /getquick /mass 123 消息 /kick /ban /template 欢迎 {name} /help")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.getenv('RAILWAY_STATIC_URL')}/webhook")
    print(f"Webhook {datetime.now().strftime('%H:%M')} +07")
