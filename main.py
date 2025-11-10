from flask import Flask, request, jsonify
import telebot
from telebot import types
import os
import sqlite3
import re
import json
import requests
from datetime import datetime
import threading
import time

app = Flask(__name__)
TOKEN = os.getenv('BOT_TOKEN', '8203814161:AAEjpp8VxdErKUwiSZCUIABLTqAzZ-lTWaY')
bot = telebot.TeleBot(TOKEN)
from datetime import datetime

app = Flask(__name__)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8203814161:AAEjpp8VxdErKUwiSZCUIABLTqAzZ-lTWaY')
bot = telebot.TeleBot(TOKEN) if TOKEN else None

# 管理员ID列表（从环境变量读取，逗号分隔）
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip().isdigit()]

# API配置
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# 数据库初始化
def init_db():
    db = sqlite3.connect('data.db', check_same_thread=False)
    c = db.cursor()
    
    # 记账表
    c.execute('CREATE TABLE IF NOT EXISTS accounts (user_id INTEGER, amount REAL, desc TEXT, time TEXT)')
    
    # 快捷回复表
    c.execute('CREATE TABLE IF NOT EXISTS quick (trigger TEXT PRIMARY KEY, response TEXT)')
    
    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        join_date TEXT,
        is_banned INTEGER DEFAULT 0
    )''')
    
    # 群组表
    c.execute('''CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        group_name TEXT,
        join_date TEXT,
        welcome_enabled INTEGER DEFAULT 1
    )''')
    
    # 消息日志表
    c.execute('''CREATE TABLE IF NOT EXISTS message_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        chat_id INTEGER,
        message TEXT,
        timestamp TEXT
    )''')
    
    # 定时消息表
    c.execute('''CREATE TABLE IF NOT EXISTS scheduled_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        message TEXT,
        schedule_time TEXT,
        repeat_interval TEXT,
        enabled INTEGER DEFAULT 1
    )''')
    
    db.commit()
    return db, c

db, c = init_db()

# 快捷回复存储
QUICK = {}
if os.path.exists('quick.json'):
    try:
        with open('quick.json', 'r', encoding='utf-8') as f:
            QUICK = json.load(f)
    except:
        QUICK = {}

def save_quick():
    with open('quick.json', 'w', encoding='utf-8') as f:
        json.dump(QUICK, f, ensure_ascii=False, indent=2)

# 保存用户信息
def save_user(user):
    try:
        c.execute('''INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, join_date)
                     VALUES (?, ?, ?, ?, ?)''',
                  (user.id, user.username or '', user.first_name or '', user.last_name or '', 
                   datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    except:
        pass

# 保存消息日志
def log_message(user_id, chat_id, text):
    try:
        c.execute('''INSERT INTO message_log (user_id, chat_id, message, timestamp)
                     VALUES (?, ?, ?, ?)''',
                  (user_id, chat_id, text[:500], datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()
    except:
        pass

# 管理员检查（增强版）
def is_admin(chat_id, user_id):
    # 检查是否在全局管理员列表
    if user_id in ADMIN_IDS:
        return True
    # 检查群组管理员
    try:
        return bot.get_chat_member(chat_id, user_id).status in ['administrator', 'creator']
    except:
        return False

# 检查是否为超级管理员
def is_super_admin(user_id):
    return user_id in ADMIN_IDS
# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "telegram-bot"}), 200

# OpenAPI specification
@app.route('/openapi.json', methods=['GET'])
def openapi_spec():
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Telegram Bot API",
            "version": "1.0.0",
            "description": "A Telegram bot with webhook and health check endpoints"
        },
        "servers": [
            {"url": "http://localhost:8080", "description": "Local server"}
        ],
        "paths": {
            "/health": {
                "get": {
                    "summary": "Health check endpoint",
                    "responses": {
                        "200": {
                            "description": "Service is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "service": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/webhook": {
                "post": {
                    "summary": "Telegram webhook endpoint",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "description": "Telegram Update object"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Webhook processed successfully"
                        }
                    }
                }
            }
        }
    }
    return jsonify(spec), 200

# Webhook 路由
@app.route('/webhook', methods=['POST'])
def webhook():
    if not bot:
        return jsonify({"error": "Bot not initialized"}), 503
    update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return '', 200

@app.route('/')
def index():
    return 'Bot is running!', 200

# ============= 第三方API集成 =============

# 天气查询
def get_weather(city):
    if not WEATHER_API_KEY:
        return "❌ 未配置天气API Key"
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=zh_cn"
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"🌤 {city} 天气\n🌡 温度: {temp}°C\n☁️ 状况: {desc}\n💧 湿度: {humidity}%"
        return "❌ 城市未找到"
    except:
        return "❌ 查询失败"

# 新闻查询
def get_news(topic='technology', country='cn'):
    if not NEWS_API_KEY:
        return "❌ 未配置新闻API Key"
    try:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&category={topic}&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.status_code == 200 and data.get('articles'):
            news_list = []
            for i, article in enumerate(data['articles'][:5], 1):
                title = article.get('title', 'No title')
                news_list.append(f"{i}. {title}")
            return "📰 最新新闻:\n\n" + "\n\n".join(news_list)
        return "❌ 未找到新闻"
    except:
        return "❌ 查询失败"

# ChatGPT集成
def ask_chatgpt(question):
    if not OPENAI_API_KEY:
        return "❌ 未配置OpenAI API Key"
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 500
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        return "❌ API调用失败"
    except Exception as e:
        return f"❌ 错误: {str(e)}"

# ============= 命令处理 =============

# 开始命令 - 设置菜单
@bot.message_handler(commands=['start'])
def start_cmd(message):
    save_user(message.from_user)
    
    # 创建命令菜单
    commands = [
        types.BotCommand("start", "开始使用机器人"),
        types.BotCommand("help", "查看帮助信息"),
        types.BotCommand("menu", "显示功能菜单"),
        types.BotCommand("add", "添加收入 /add 金额 描述"),
        types.BotCommand("sub", "添加支出 /sub 金额 描述"),
        types.BotCommand("balance", "查询余额"),
        types.BotCommand("weather", "查询天气 /weather 城市"),
        types.BotCommand("news", "获取最新新闻"),
        types.BotCommand("ask", "问ChatGPT /ask 问题"),
        types.BotCommand("setquick", "设置快捷回复"),
        types.BotCommand("getquick", "查看快捷回复"),
    ]
    
    try:
        bot.set_my_commands(commands)
    except:
        pass
    
    # 发送欢迎消息与内联键盘
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 记账", callback_data="menu_account"),
        types.InlineKeyboardButton("💬 快捷回复", callback_data="menu_quick"),
        types.InlineKeyboardButton("🌐 API服务", callback_data="menu_api"),
        types.InlineKeyboardButton("👥 群管理", callback_data="menu_group"),
        types.InlineKeyboardButton("❓ 帮助", callback_data="menu_help")
    )
    
    welcome_text = f"""
🤖 欢迎使用智能机器人！

👋 你好 {message.from_user.first_name}！

✨ 主要功能：
• 📊 记账管理
• 💬 快捷回复
• 🌐 第三方API集成
• 👥 群聊管理
• 📢 消息群发

点击下方按钮或发送 /help 查看详细命令
"""
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# 菜单命令
@bot.message_handler(commands=['menu'])
def menu_cmd(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 记账", callback_data="menu_account"),
        types.InlineKeyboardButton("💬 快捷回复", callback_data="menu_quick"),
        types.InlineKeyboardButton("🌐 API服务", callback_data="menu_api"),
        types.InlineKeyboardButton("👥 群管理", callback_data="menu_group"),
        types.InlineKeyboardButton("❓ 帮助", callback_data="menu_help")
    )
    bot.send_message(message.chat.id, "📋 请选择功能：", reply_markup=markup)

# 内联键盘回调处理
@bot.callback_query_handler(func=lambda call: call.data.startswith('menu_'))
def menu_callback(call):
    if call.data == "menu_account":
        text = """
📊 记账功能

命令列表：
• /add 金额 描述 - 添加收入
• /sub 金额 描述 - 添加支出  
• /balance - 查询余额
• 直接发送数字 - 快速记账

示例：
/add 1000 工资
/sub 50 午餐
100
"""
    elif call.data == "menu_quick":
        text = """
💬 快捷回复功能

命令列表：
• /setquick 触发词 回复内容
• /getquick - 查看所有快捷回复
• /delquick 触发词 - 删除快捷回复

示例：
/setquick hi 你好！很高兴见到你
"""
    elif call.data == "menu_api":
        text = """
🌐 第三方API服务

可用服务：
• /weather 城市 - 查询天气
• /news - 获取最新新闻
• /ask 问题 - 问ChatGPT

示例：
/weather 北京
/news
/ask 什么是人工智能？
"""
    elif call.data == "menu_group":
        text = """
👥 群聊管理功能

命令列表：
• /kick - 踢出用户（回复消息）
• /ban - 封禁用户（回复消息）
• /unban - 解封用户
• /mute - 禁言用户
• /warn - 警告用户
• /template - 设置欢迎消息

管理员专用：
• /mass - 群发消息
• /schedule - 定时消息
"""
    else:  # menu_help
        text = """
❓ 帮助信息

🤖 机器人功能说明：

1️⃣ 自动回复
发送消息自动触发快捷回复

2️⃣ 记账管理  
追踪收支，查询余额

3️⃣ API集成
天气、新闻、ChatGPT

4️⃣ 群聊管理
踢人、封禁、定时消息

5️⃣ 群发消息
管理员可群发通知

发送 /start 返回主菜单
"""
    
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)
# ============= 第三方API命令 =============

# 天气命令
@bot.message_handler(commands=['weather'])
def weather_cmd(message):
    save_user(message.from_user)
    try:
        city = ' '.join(message.text.split()[1:])
        if not city:
            bot.reply_to(message, "❌ 请输入城市名，如：/weather 北京")
            return
        result = get_weather(city)
        bot.reply_to(message, result)
    except:
        bot.reply_to(message, "❌ 格式错误，使用：/weather 城市名")

# 新闻命令
@bot.message_handler(commands=['news'])
def news_cmd(message):
    save_user(message.from_user)
    bot.send_message(message.chat.id, "🔍 正在获取最新新闻...")
    result = get_news()
    bot.send_message(message.chat.id, result)

# ChatGPT命令
@bot.message_handler(commands=['ask'])
def ask_cmd(message):
    save_user(message.from_user)
    try:
        question = ' '.join(message.text.split()[1:])
        if not question:
            bot.reply_to(message, "❌ 请输入问题，如：/ask 什么是AI？")
            return
        bot.send_message(message.chat.id, "🤔 正在思考...")
        result = ask_chatgpt(question)
        bot.send_message(message.chat.id, f"💭 ChatGPT回答：\n\n{result}")
    except:
        bot.reply_to(message, "❌ 格式错误，使用：/ask 你的问题")

# ============= 记账功能 =============

# 记账命令（增强版）
@bot.message_handler(commands=['add', 'sub', 'balance'])
def account_cmd(message):
    save_user(message.from_user)
    cmd = message.text.split()[0][1:]
    try:
        if cmd == 'balance':
            c.execute("SELECT SUM(amount) FROM accounts WHERE user_id=?", (message.from_user.id,))
            total = c.fetchone()[0] or 0
            
            # 获取最近5条记录
            c.execute("SELECT amount, desc, time FROM accounts WHERE user_id=? ORDER BY rowid DESC LIMIT 5", 
                     (message.from_user.id,))
            recent = c.fetchall()
            
            result = f"💰 当前余额: {total:.2f}\n\n📊 最近记录："
            for amount, desc, time_str in recent:
                result += f"\n{'➕' if amount > 0 else '➖'} {abs(amount):.2f} | {desc} | {time_str}"
            
            bot.reply_to(message, result)
        else:
            amount = float(message.text.split()[1])
            desc = ' '.join(message.text.split()[2:]) or '无描述'
            timestamp = datetime.now().strftime("%m-%d %H:%M")
            c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)",
                      (message.from_user.id, amount if cmd == 'add' else -amount, desc, timestamp))
            db.commit()
            bot.reply_to(message, f"✅ {'收入' if cmd == 'add' else '支出'}: {amount} | {desc} | {timestamp}")
    except Exception as e:
        bot.reply_to(message, f"❌ 格式: /{cmd} 金额 描述\n示例: /add 100 工资")

# ============= 快捷回复管理 =============

# 快捷回复命令（增强版）
@bot.message_handler(commands=['setquick', 'getquick', 'delquick'])
def quick_cmd(message):
    save_user(message.from_user)
    cmd = message.text.split()[0][1:]
    try:
        if cmd == 'getquick':
            if not QUICK:
                bot.reply_to(message, "📋 暂无快捷回复")
            else:
                result = "📋 快捷回复列表：\n\n"
                for k, v in QUICK.items():
                    if k != 'template':
                        result += f"🔹 {k} → {v}\n"
                bot.reply_to(message, result)
        elif cmd == 'delquick':
            trigger = message.text.split()[1].lower()
            if trigger in QUICK:
                del QUICK[trigger]
                save_quick()
                bot.reply_to(message, f"✅ 已删除快捷回复: {trigger}")
            else:
                bot.reply_to(message, f"❌ 未找到快捷回复: {trigger}")
        else:  # setquick
            parts = message.text.split(maxsplit=2)
            if len(parts) < 3:
                bot.reply_to(message, "❌ 格式: /setquick 触发词 回复内容")
                return
            trigger, response = parts[1].lower(), parts[2]
            QUICK[trigger] = response
            save_quick()
            
            # 创建确认按钮
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📝 查看所有", callback_data="menu_quick"))
            
            bot.reply_to(message, f"✅ 快捷回复已设置\n🔹 {trigger} → {response}", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"❌ 操作失败: {str(e)}")

# 回复模板
@bot.message_handler(commands=['template'])
def set_template(message):
    save_user(message.from_user)
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ 仅限管理员使用！")
    try:
        template = ' '.join(message.text.split()[1:])
        if not template:
            return bot.reply_to(message, "❌ 请输入模板，如 /template 欢迎 {name}")
        QUICK['template'] = template
        save_quick()
        bot.reply_to(message, f"✅ 模板设为: {template}")
    except:
        bot.reply_to(message, "❌ 格式: /template 文本")

# ============= 群聊管理 =============

# 群管理命令（增强版）
@bot.message_handler(commands=['kick', 'ban', 'unban', 'mute', 'warn'])
def manage_group(message):
    save_user(message.from_user)
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ 仅限管理员使用！")
    
    cmd = message.text.split()[0][1:]
    
    try:
        # 获取目标用户
        if message.reply_to_message:
            target_id = message.reply_to_message.from_user.id
            target_name = message.reply_to_message.from_user.first_name
        else:
            target_id = int(message.text.split()[1])
            target_name = str(target_id)
        
        if cmd == 'kick':
            bot.kick_chat_member(message.chat.id, target_id)
            bot.unban_chat_member(message.chat.id, target_id)
            bot.reply_to(message, f"✅ 已踢出 {target_name}")
        elif cmd == 'ban':
            bot.kick_chat_member(message.chat.id, target_id)
            bot.reply_to(message, f"✅ 已封禁 {target_name}")
        elif cmd == 'unban':
            bot.unban_chat_member(message.chat.id, target_id)
            bot.reply_to(message, f"✅ 已解封 {target_name}")
        elif cmd == 'mute':
            # 禁言1小时
            bot.restrict_chat_member(message.chat.id, target_id, 
                                    until_date=int(time.time() + 3600),
                                    can_send_messages=False)
            bot.reply_to(message, f"✅ 已禁言 {target_name} (1小时)")
        elif cmd == 'warn':
            bot.reply_to(message, f"⚠️ 警告 {target_name}\n请遵守群规！")
    except Exception as e:
        bot.reply_to(message, f"❌ 操作失败: {str(e)}")

# 群发消息（仅限超级管理员）
@bot.message_handler(commands=['mass'])
def mass_cmd(message):
    save_user(message.from_user)
    if not is_super_admin(message.from_user.id):
        return bot.reply_to(message, "❌ 仅限超级管理员使用！")
    
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            return bot.reply_to(message, "❌ 格式: /mass user_id1,user_id2 消息内容")
        
        # 解析用户ID和消息
        args = parts[1].split(maxsplit=1)
        if len(args) < 2:
            return bot.reply_to(message, "❌ 格式: /mass user_id1,user_id2 消息内容")
        
        target_ids = [int(x.strip()) for x in args[0].split(',') if x.strip().isdigit()]
        msg_content = args[1]
        
        success = 0
        for target_id in target_ids:
            try:
                bot.send_message(target_id, f"📢 系统消息：\n\n{msg_content}")
                success += 1
            except:
                pass
        
        bot.reply_to(message, f"📬 群发完成: {success}/{len(target_ids)}")
    except Exception as e:
        bot.reply_to(message, f"❌ 操作失败: {str(e)}")

# 定时消息
@bot.message_handler(commands=['schedule'])
def schedule_cmd(message):
    save_user(message.from_user)
    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "❌ 仅限管理员使用！")
    
    bot.reply_to(message, "⏰ 定时消息功能开发中...")

# 欢迎新成员（增强版）
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for user in message.new_chat_members:
        save_user(user)
        
        if 'template' in QUICK:
            welcome_msg = QUICK['template'].replace('{name}', user.first_name)
        else:
            welcome_msg = f"欢迎 {user.first_name} 加入群组！"
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📋 群规", callback_data="group_rules"))
        
        bot.send_message(message.chat.id, 
                        f"🎉 {welcome_msg}\n⏰ {datetime.now().strftime('%H:%M')}",
                        reply_markup=markup)

# 成员离开
@bot.message_handler(content_types=['left_chat_member'])
def member_left(message):
    user = message.left_chat_member
    bot.send_message(message.chat.id, f"👋 {user.first_name} 离开了群组")

# ============= 自动回复 =============

# 自动回复（增强版）
@bot.message_handler(content_types=['text'])
def auto_reply(message):
    save_user(message.from_user)
    log_message(message.from_user.id, message.chat.id, message.text)
    
    text = message.text.lower()
    user_id = message.from_user.id
    
    # 正则匹配金额格式（如 10.5 或 10）
    if match := re.match(r'^\d+(\.\d+)?$', text):
        amount = float(match.group())
        timestamp = datetime.now().strftime("%m-%d %H:%M")
        c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", 
                 (user_id, amount, '自动记账', timestamp))
        db.commit()
        bot.reply_to(message, f"✅ 自动记账: {amount} | {timestamp}")
    # 快捷回复
    elif trigger := next((k for k in QUICK if k != 'template' and k in text), None):
        bot.reply_to(message, QUICK[trigger])
    # 智能响应
    elif any(word in text for word in ['你好', 'hi', 'hello']):
        bot.reply_to(message, f"你好 {message.from_user.first_name}！有什么可以帮助你的吗？\n发送 /menu 查看功能")
    elif any(word in text for word in ['谢谢', 'thanks', '感谢']):
        bot.reply_to(message, "不客气！很高兴能帮到你 😊")
    elif '?' in text or '吗' in text:
        bot.reply_to(message, "这是个好问题！你可以使用 /ask 命令来获得更详细的回答")

# 帮助命令（增强版）
@bot.message_handler(commands=['help'])
def help_cmd(message):
    save_user(message.from_user)
    help_text = """
📖 机器人帮助

📊 记账功能：
/add 金额 描述 - 添加收入
/sub 金额 描述 - 添加支出
/balance - 查询余额

💬 快捷回复：
/setquick 触发词 回复 - 设置
/getquick - 查看列表
/delquick 触发词 - 删除

🌐 API服务：
/weather 城市 - 查天气
/news - 看新闻
/ask 问题 - 问ChatGPT

👥 群管理（管理员）：
/kick - 踢出用户
/ban - 封禁用户
/unban - 解封用户
/mute - 禁言用户
/warn - 警告用户
/template 模板 - 设置欢迎语
/mass ID列表 消息 - 群发

📱 其他命令：
/start - 开始使用
/menu - 显示菜单
/help - 显示帮助

💡 提示：直接发送数字可快速记账！
"""
    bot.reply_to(message, help_text)

# ============= 启动 =============

if __name__ == "__main__":
    try:
        # 移除旧的webhook
        bot.remove_webhook()
        
        # 设置新的webhook
        webhook_url = f"https://{os.getenv('RAILWAY_STATIC_URL', 'localhost')}/webhook"
        bot.set_webhook(url=webhook_url)
        
        print(f"✅ Bot started successfully!")
        print(f"🔗 Webhook: {webhook_url}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 启动Flask服务器
        port = int(os.getenv('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Error starting bot: {str(e)}")

# 自动回复
if bot:
    @bot.message_handler(content_types=['text'])
    def auto_reply(message):
        text = message.text.lower()
        user_id = message.from_user.id
        # 正则匹配金额格式（如 10.5 或 10）
        if match := re.match(r'^\d+(\.\d+)?$', text):
            amount = float(match.group())
            c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (user_id, amount, '自动记账', '17:18'))
            db.commit()
            bot.reply_to(message, f"✅ 自动记 {amount} | 17:18 +07")
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
    # Set up bot webhook if bot is initialized and RAILWAY_STATIC_URL is set
    if bot and os.getenv('RAILWAY_STATIC_URL'):
        try:
            bot.remove_webhook()
            bot.set_webhook(url=f"https://{os.getenv('RAILWAY_STATIC_URL')}/webhook")
            print(f"Webhook configured for {os.getenv('RAILWAY_STATIC_URL')}")
        except Exception as e:
            print(f"Warning: Failed to set webhook: {e}")
    
    # Run Flask app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
