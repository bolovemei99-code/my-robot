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
# My Robot - Telegram Bot

一个功能强大的 Telegram 机器人，支持记账、群管理、快捷回复、第三方API集成等功能。

A powerful Telegram bot with accounting, group management, quick reply, and third-party API integration features.

📚 **[查看详细功能文档 / View Detailed Features](FEATURES.md)**

## 功能特性 / Features

### 📊 记账功能 / Accounting
- ✅ 自动识别金额并记账
- ✅ 支持添加收入和支出
- ✅ 查询账户余额和历史记录
- ✅ 记录交易描述和时间

### 💬 快捷回复 / Quick Reply
- ✅ 自定义触发词和回复
- ✅ Telegram原生命令菜单
- ✅ 内联键盘交互界面
- ✅ 智能关键词识别

### 👥 群管理 / Group Management
- ✅ 踢出/封禁/解封用户 (`/kick`, `/ban`, `/unban`)
- ✅ 禁言和警告 (`/mute`, `/warn`)
- ✅ 管理员权限验证
- ✅ 新成员欢迎消息（支持模板变量）
- ✅ 成员离开通知

### 🌐 第三方API集成 / Third-party API Integration
- ✅ 天气查询 (`/weather`) - OpenWeatherMap
- ✅ 新闻获取 (`/news`) - NewsAPI
- ✅ ChatGPT问答 (`/ask`) - OpenAI

### 📢 群发消息 / Mass Messaging
- ✅ 批量发送消息给指定用户
- ✅ 超级管理员权限控制
- ✅ 发送状态反馈

### 💾 数据库支持 / Database Support
- ✅ 用户信息存储
- ✅ 群组信息管理
- ✅ 消息日志记录
- ✅ 记账数据持久化
- ✅ 定时消息支持（开发中）

## 快速开始 / Quick Start

### 方法一：Railway 一键部署 / Railway One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. 点击上方按钮
2. 设置环境变量（至少需要 `BOT_TOKEN`）
3. 部署完成！

### 方法二：本地运行 / Run Locally

1. **克隆仓库 / Clone the repository:**
# Telegram 机器人 (My Robot)

一个简单的 Telegram 自动回复机器人。

## 功能

- 自动回复特定关键词
- 支持以下回复规则：
  - "hi" → "你好！"
  - "hello" → "嗨！"
  - "bye" → "再见！"
  - "帮助" → "发 hi 试试自动回复"
- 默认回复：对其他消息回复 "我听到了！"

## 部署方式

### 方式一：Docker 部署（推荐）

#### 前提条件
- 安装 Docker 和 Docker Compose
- 获取 Telegram Bot Token（从 @BotFather 获取）

#### 步骤

1. 克隆仓库
```bash
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot
```

2. **安装依赖 / Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **配置环境变量 / Configure environment variables:**
```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的配置
nano .env
```

必需配置：
- `BOT_TOKEN`: 从 [@BotFather](https://t.me/BotFather) 获取

可选配置：
- `ADMIN_IDS`: 超级管理员ID（逗号分隔）
- `WEATHER_API_KEY`: 天气API密钥
- `NEWS_API_KEY`: 新闻API密钥  
- `OPENAI_API_KEY`: OpenAI API密钥

4. **运行机器人 / Run the bot:**
```bash
python main.py
```

## 命令列表 / Commands

### 基础命令 / Basic Commands
| 命令 / Command | 说明 / Description | 示例 / Example |
|----------------|-------------------|----------------|
| `/start` | 开始使用，显示欢迎菜单 / Start bot | `/start` |
| `/menu` | 显示功能菜单 / Show menu | `/menu` |
| `/help` | 查看帮助信息 / Show help | `/help` |

### 记账命令 / Accounting Commands
| 命令 / Command | 说明 / Description | 示例 / Example |
|----------------|-------------------|----------------|
| `/add <金额> <描述>` | 添加收入 / Add income | `/add 100 工资` |
| `/sub <金额> <描述>` | 添加支出 / Add expense | `/sub 50 午餐` |
| `/balance` | 查询余额 / Check balance | `/balance` |
| `数字` | 快速记账 / Quick accounting | `100` |

### 快捷回复命令 / Quick Reply Commands
| 命令 / Command | 说明 / Description | 示例 / Example |
|----------------|-------------------|----------------|
| `/setquick <触发词> <回复>` | 设置快捷回复 / Set quick reply | `/setquick hi 你好` |
| `/getquick` | 查看所有快捷回复 / View all quick replies | `/getquick` |
| `/delquick <触发词>` | 删除快捷回复 / Delete quick reply | `/delquick hi` |

### API服务命令 / API Service Commands
| 命令 / Command | 说明 / Description | 示例 / Example |
|----------------|-------------------|----------------|
| `/weather <城市>` | 查询天气 / Check weather | `/weather 北京` |
| `/news` | 获取最新新闻 / Get news | `/news` |
| `/ask <问题>` | 问ChatGPT / Ask ChatGPT | `/ask 什么是AI？` |

### 群管理命令 / Group Management Commands (管理员 / Admin Only)
| 命令 / Command | 说明 / Description | 示例 / Example |
|----------------|-------------------|----------------|
| `/kick` | 踢出用户 / Kick user | `/kick` (回复消息) |
| `/ban` | 封禁用户 / Ban user | `/ban` (回复消息) |
| `/unban` | 解封用户 / Unban user | `/unban` (回复消息) |
| `/mute` | 禁言用户(1小时) / Mute user | `/mute` (回复消息) |
| `/warn` | 警告用户 / Warn user | `/warn` (回复消息) |
| `/template <模板>` | 设置欢迎模板 / Set welcome template | `/template 欢迎 {name}` |

### 超级管理员命令 / Super Admin Commands
| 命令 / Command | 说明 / Description | 示例 / Example |
|----------------|-------------------|----------------|
| `/mass <ID列表> <消息>` | 群发消息 / Mass message | `/mass 123,456 通知` |
| `/schedule` | 定时消息 / Schedule message | `/schedule`(开发中) |

## 使用示例 / Usage Examples

### 💬 智能对话
```
用户: 你好
机器人: 你好 张三！有什么可以帮助你的吗？
       发送 /menu 查看功能

用户: 100
机器人: ✅ 自动记账: 100 | 11-10 14:30
```

### 📊 记账管理
```
用户: /add 1000 工资
机器人: ✅ 收入: 1000 | 工资 | 11-10 14:30

用户: /sub 50 午餐
机器人: ✅ 支出: 50 | 午餐 | 11-10 12:00

用户: /balance
机器人: 💰 当前余额: 950.00

       📊 最近记录：
       ➖ 50.00 | 午餐 | 11-10 12:00
       ➕ 1000.00 | 工资 | 11-10 14:30
```

### 🌐 API服务
```
用户: /weather 北京
机器人: 🌤 北京 天气
       🌡 温度: 15°C
       ☁️ 状况: 晴
       💧 湿度: 60%

用户: /ask 什么是人工智能？
机器人: 🤔 正在思考...
       💭 ChatGPT回答：
       人工智能(AI)是计算机科学的一个分支...
```

### 👥 群组管理
```
管理员: /template 欢迎 {name} 加入我们的大家庭！
机器人: ✅ 模板设为: 欢迎 {name} 加入我们的大家庭！

[新用户加入]
机器人: 🎉 欢迎 李四 加入我们的大家庭！
       ⏰ 14:30
       [📋 群规]

管理员: /kick [回复某用户消息]
机器人: ✅ 已踢出 李四
```

## 项目结构 / Project Structure

```
my-robot/
├── main.py              # 主程序文件 / Main program
├── requirements.txt     # Python依赖 / Dependencies
├── Procfile            # 部署配置 / Deployment config
├── mcp.json            # MCP服务器配置 / MCP config
├── README.md           # 项目说明 / Project readme
├── FEATURES.md         # 功能详细文档 / Detailed features
├── LICENSE             # MIT许可证 / License
├── .env.example        # 环境变量示例 / Env example
├── .gitignore          # Git忽略文件 / Git ignore
├── data.db             # SQLite数据库 (自动生成)
└── quick.json          # 快捷回复数据 (自动生成)
```

## 技术架构 / Technical Architecture

### 核心技术栈
- **Python 3.7+**: 主要编程语言
- **pyTelegramBotAPI**: Telegram Bot API封装
- **Flask**: Web框架（处理Webhook）
- **SQLite3**: 轻量级数据库
- **Requests**: HTTP请求库

### 数据库设计
- `accounts`: 记账数据表
- `users`: 用户信息表
- `groups`: 群组信息表
- `message_log`: 消息日志表
- `scheduled_messages`: 定时消息表
- `quick`: 快捷回复表

### API集成
- **OpenWeatherMap**: 天气数据
- **NewsAPI**: 新闻数据
- **OpenAI**: ChatGPT对话

## 环境变量配置 / Environment Configuration

创建 `.env` 文件并配置以下变量：

```bash
# 必需 / Required
BOT_TOKEN=your_telegram_bot_token

# 可选 / Optional
ADMIN_IDS=123456789,987654321
WEATHER_API_KEY=your_weather_api_key
NEWS_API_KEY=your_news_api_key
OPENAI_API_KEY=your_openai_api_key
RAILWAY_STATIC_URL=your-app.railway.app
PORT=5000
```

### 获取API Keys
- **BOT_TOKEN**: [@BotFather](https://t.me/BotFather)
- **WEATHER_API_KEY**: [OpenWeatherMap](https://openweathermap.org/api)
- **NEWS_API_KEY**: [NewsAPI](https://newsapi.org/)
- **OPENAI_API_KEY**: [OpenAI Platform](https://platform.openai.com/)

## 安全提示 / Security Notes

⚠️ **重要安全建议 / Important Security Tips**: 

- 🔐 **不要泄露Token**: 永远不要将 Bot Token 提交到公共仓库
- 🔑 **保护API Keys**: 使用环境变量存储所有敏感信息
- 💾 **定期备份**: 定期备份 `data.db` 和 `quick.json` 文件
- 👥 **限制管理员**: 谨慎设置超级管理员权限
- 🔄 **定期更新**: 保持依赖包为最新版本
- 📝 **监控日志**: 定期检查机器人操作日志
- 🚫 **用户验证**: 在群组中启用用户验证功能

## 部署指南 / Deployment Guide

### Railway 部署（推荐）

1. Fork 本仓库到你的 GitHub
2. 访问 [Railway](https://railway.app/)
3. 选择 "New Project" → "Deploy from GitHub repo"
4. 选择你的仓库
5. 添加环境变量（至少添加 `BOT_TOKEN`）
6. 等待自动部署完成

### Heroku 部署

```bash
# 登录 Heroku
heroku login

# 创建应用
heroku create your-bot-name

# 设置环境变量
heroku config:set BOT_TOKEN=your_token
heroku config:set ADMIN_IDS=your_admin_ids

# 部署
git push heroku main

# 查看日志
heroku logs --tail
```

### Docker 部署

创建 `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

运行:
```bash
docker build -t telegram-bot .
docker run -d --env-file .env -p 5000:5000 telegram-bot
```

## 开发指南 / Development Guide

### 本地开发环境设置

```bash
# 克隆仓库
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 运行
python main.py
```

### 添加新功能

1. 在 `main.py` 中添加新的处理器
2. 更新命令菜单（如需要）
3. 测试功能
4. 更新文档
5. 提交 Pull Request

### 测试建议

- 测试所有命令是否正常工作
- 测试权限控制是否有效
- 测试数据库读写是否正常
- 测试API调用是否成功
- 测试错误处理是否完善

## 许可证 / License

MIT License - 详见 LICENSE 文件 / See LICENSE file for details

## 联系方式 / Contact

如有问题或建议，请提交 Issue。
For questions or suggestions, please submit an Issue.
2. 设置环境变量
```bash
export TG_TOKEN="your_telegram_bot_token_here"
```

或者创建 `.env` 文件：
```
TG_TOKEN=your_telegram_bot_token_here
```

3. 使用 Docker Compose 启动
```bash
docker-compose up -d
```

4. 查看日志
```bash
docker-compose logs -f
```

5. 停止机器人
```bash
docker-compose down
```

### 方式二：直接运行

#### 前提条件
- Python 3.12 或更高版本
- pip

#### 步骤

1. 克隆仓库
```bash
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 设置环境变量并运行
```bash
export TG_TOKEN="your_telegram_bot_token_here"
python main.py
```

### 方式三：使用 Docker 手动构建

```bash
# 构建镜像
docker build -t telegram-bot .

# 运行容器
docker run -d \
  --name my-robot \
  --restart unless-stopped \
  -e TG_TOKEN="your_telegram_bot_token_here" \
  telegram-bot
```

## 开发

### 本地开发环境设置

1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行机器人
```bash
export TG_TOKEN="your_telegram_bot_token_here"
python main.py
```

## CI/CD

本项目使用 GitHub Actions 进行持续集成和部署：

- 每次推送到 `main` 分支时自动运行测试
- 自动构建 Docker 镜像
- Pull Request 也会触发测试

查看工作流状态：`.github/workflows/deploy.yml`

## 配置

### 环境变量

- `TG_TOKEN` (必需): Telegram Bot Token，从 @BotFather 获取

### 修改回复规则

编辑 `main.py` 中的 `REPLIES` 字典：

```python
REPLIES = {
    "hi": "你好！",
    "hello": "嗨！",
    "bye": "再见！",
    "帮助": "发 hi 试试自动回复"
}
```

## 故障排除

### 机器人无响应
- 检查 `TG_TOKEN` 是否正确设置
- 确认 Token 有效（在 @BotFather 中检查）
- 查看日志输出是否有错误信息

### Docker 容器无法启动
- 检查 Docker 是否正在运行
- 确认环境变量已正确传递
- 使用 `docker logs my-robot` 查看错误信息

## 许可证

本项目为个人学习项目。

## 联系方式

如有问题，请提交 Issue。
