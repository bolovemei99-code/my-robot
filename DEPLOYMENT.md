# 部署指南 (Deployment Guide)

## 准备工作 (Prerequisites)

### 1. 获取 Telegram Bot Token
1. 在 Telegram 中找到 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 创建新机器人（或使用现有的）
3. 按照指示设置机器人名称和用户名
4. 保存 BotFather 给你的 Token（格式类似：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

### 2. 环境要求
- Python 3.8 或更高版本
- aiogram 3.13.1

## 本地部署 (Local Deployment)

### 步骤 1: 安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 2: 设置环境变量
```bash
# Linux/Mac
export BOT_TOKEN="your_bot_token_here"

# Windows CMD
set BOT_TOKEN=your_bot_token_here

# Windows PowerShell
$env:BOT_TOKEN="your_bot_token_here"
```

### 步骤 3: 运行机器人
```bash
python bot.py
```

如果看到 "机器人正在启动..." 消息，说明机器人已成功启动。

## Heroku 部署 (Heroku Deployment)

### 步骤 1: 安装 Heroku CLI
访问 https://devcenter.heroku.com/articles/heroku-cli 下载并安装

### 步骤 2: 登录 Heroku
```bash
heroku login
```

### 步骤 3: 创建 Heroku 应用
```bash
heroku create your-app-name
```

### 步骤 4: 设置环境变量
```bash
heroku config:set BOT_TOKEN="your_bot_token_here" -a your-app-name
```

### 步骤 5: 部署到 Heroku
```bash
git push heroku main
```
或如果你在其他分支：
```bash
git push heroku your-branch-name:main
```

### 步骤 6: 启动 worker
```bash
heroku ps:scale worker=1 -a your-app-name
```

### 步骤 7: 查看日志
```bash
heroku logs --tail -a your-app-name
```

## Docker 部署 (Docker Deployment)

### 创建 Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]
```

### 构建和运行
```bash
# 构建镜像
docker build -t my-telegram-bot .

# 运行容器
docker run -e BOT_TOKEN="your_bot_token_here" my-telegram-bot
```

## 验证部署 (Verify Deployment)

1. 在 Telegram 中找到你的机器人
2. 发送 `/start` 命令
3. 应该收到回复："你好！我是你的新机器人！"
4. 发送任何其他消息，机器人应该会回显你的消息

## 故障排除 (Troubleshooting)

### ImportError: cannot import name 'executor'
✓ 已修复：代码已迁移到 aiogram 3.x API

### ValueError: BOT_TOKEN environment variable is required
确保设置了 BOT_TOKEN 环境变量

### 机器人不响应
1. 检查机器人是否在线：查看日志中的 "机器人正在启动..." 消息
2. 确认 Token 正确
3. 检查网络连接

## 代码说明 (Code Overview)

### 主要改动（aiogram 2.x → 3.x）
- ❌ `from aiogram.utils import executor` → ✓ `import asyncio`
- ❌ `Dispatcher(bot)` → ✓ `Dispatcher()`
- ❌ `@dp.message_handler(commands=['start'])` → ✓ `@dp.message(Command('start'))`
- ❌ `executor.start_polling(dp)` → ✓ `asyncio.run(main())`

### 安全性
- Token 仅从环境变量读取，不硬编码在代码中
- 如果未设置 BOT_TOKEN，机器人将拒绝启动并显示清晰的错误消息

## 支持 (Support)

如有问题，请在 GitHub 仓库中提交 Issue。
