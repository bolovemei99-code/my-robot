# Telegram Bot - Railway Deployment

一个简单的 Telegram 自动回复机器人，支持部署到 Railway。

## 功能特点

- 自动回复关键词：hi, hello, bye, 帮助
- 支持 Webhook 模式，适合云平台部署
- 使用 Flask 作为 Web 服务器

## Railway 部署步骤

### 1. 上传文件到 GitHub
确保以下文件已上传到 GitHub 仓库：
- `main.py` - 机器人主程序
- `requirements.txt` - Python 依赖
- `Procfile` - Railway 配置文件
- `.gitignore` - Git 忽略文件

### 2. 在 Railway 创建项目
1. 访问 [Railway.app](https://railway.app/)
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择你的 `my-robot` 仓库

### 3. 配置环境变量
在 Railway 项目中：
1. 进入 "Settings" > "Variables"
2. 添加环境变量：
   - `TG_TOKEN`: 你的 Telegram Bot Token（从 @BotFather 获取）

### 4. 生成公开域名
1. 进入 "Networking" 标签
2. 点击 "Generate Domain"
3. 复制生成的域名（例如：`your-app.railway.app`）

### 5. 设置 Webhook
部署完成后，访问以下 URL 来配置 Telegram Webhook：
```
https://your-app.railway.app/setWebhook
```
如果看到 "Webhook set to ..." 的消息，说明配置成功。

### 6. 测试机器人
1. 在 Telegram 中找到你的机器人
2. 发送私聊消息 "hi"
3. 机器人应该回复 "你好！"

## 本地开发

如果要在本地测试，需要安装依赖：

```bash
pip install -r requirements.txt
```

设置环境变量：
```bash
export TG_TOKEN="your_bot_token"
export RAILWAY_PUBLIC_DOMAIN="your-domain.railway.app"
export PORT=5000
```

运行：
```bash
python main.py
```

## 自动回复规则

当前支持的关键词：
- "hi" → "你好！"
- "hello" → "嗨！"
- "bye" → "再见！"
- "帮助" → "发 hi 试试自动回复"

其他消息会收到默认回复："我听到了！"

## 技术栈

- Python 3
- pyTelegramBotAPI - Telegram Bot API 库
- Flask - Web 框架
- Railway - 部署平台
