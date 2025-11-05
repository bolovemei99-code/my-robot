import os
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量读取 Token
BOT_TOKEN = os.getenv('8424353653:AAFAgNubsDb1xwGEtwkelH6OYc3JwdynD5Y')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """处理 /start 命令"""
    welcome_text = (
        "👋 你好！我是你的新机器人！\n\n"
        "我可以帮你做很多事情。\n"
        "使用 /help 查看所有可用命令。"
    )
    await message.reply(welcome_text)
    logger.info(f"用户 {message.from_user.id} 启动了机器人")

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    """显示帮助信息"""
    help_text = (
        "📚 *可用命令列表：*\n\n"
        "/start - 启动机器人\n"
        "/help - 显示此帮助信息\n"
        "/info - 显示你的用户信息\n"
        "/time - 显示当前时间\n"
        "/calc <表达式> - 计算数学表达式\n"
        "例如: /calc 2+2*3\n\n"
        "💬 发送任何消息，我会重复它！"
    )
    await message.reply(help_text, parse_mode='Markdown')
    logger.info(f"用户 {message.from_user.id} 请求帮助")

@dp.message_handler(commands=['info'])
async def info_command(message: types.Message):
    """显示用户信息"""
    user = message.from_user
    info_text = (
        "👤 *你的信息：*\n\n"
        f"ID: `{user.id}`\n"
        f"用户名: @{user.username if user.username else '未设置'}\n"
        f"姓名: {user.full_name}\n"
        f"语言: {user.language_code if user.language_code else '未知'}\n"
    )
    await message.reply(info_text, parse_mode='Markdown')
    logger.info(f"用户 {message.from_user.id} 查询信息")

@dp.message_handler(commands=['time'])
async def time_command(message: types.Message):
    """显示当前时间"""
    now = datetime.now()
    time_text = (
        "🕐 *当前时间：*\n\n"
        f"日期: {now.strftime('%Y年%m月%d日')}\n"
        f"时间: {now.strftime('%H:%M:%S')}\n"
        f"星期: {['一', '二', '三', '四', '五', '六', '日'][now.weekday()]}"
    )
    await message.reply(time_text, parse_mode='Markdown')
    logger.info(f"用户 {message.from_user.id} 查询时间")

@dp.message_handler(commands=['calc'])
async def calc_command(message: types.Message):
    """计算数学表达式"""
    try:
        # 获取命令后的表达式
        expression = message.text.replace('/calc', '').strip()
        if not expression:
            await message.reply("❌ 请提供一个数学表达式\n例如: /calc 2+2*3")
            return
        
        # 安全的计算，只允许基本数学运算
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            await message.reply("❌ 表达式只能包含数字和基本运算符 (+, -, *, /, ())")
            return
        
        result = eval(expression)
        result_text = f"🧮 *计算结果：*\n\n`{expression}` = `{result}`"
        await message.reply(result_text, parse_mode='Markdown')
        logger.info(f"用户 {message.from_user.id} 计算: {expression} = {result}")
    except ZeroDivisionError:
        await message.reply("❌ 错误：除数不能为零")
    except Exception as e:
        await message.reply(f"❌ 计算错误：表达式无效\n{str(e)}")
        logger.error(f"计算错误: {e}")

@dp.message_handler()
async def echo(message: types.Message):
    """回显用户消息"""
    await message.answer(f"🔄 你说: {message.text}")
    logger.info(f"用户 {message.from_user.id} 发送消息: {message.text[:50]}")

@dp.errors_handler()
async def errors_handler(update, exception):
    """处理错误"""
    logger.error(f'发生错误: {exception}')
    return True

if __name__ == '__main__':
    logger.info("机器人正在启动...")
    print("机器人正在启动...")
    executor.start_polling(dp, skip_updates=True)
