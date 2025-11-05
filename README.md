# My Robot - Telegram Bot

一个使用 aiogram 3.x 构建的简单 Telegram 机器人。

A simple Telegram bot built with aiogram 3.x.

## 功能 (Features)

- `/start` - 欢迎消息
- 回声功能 - 机器人会重复你发送的任何消息

## 技术栈 (Tech Stack)

- Python 3.8+
- aiogram 3.13.1
- asyncio

## 快速开始 (Quick Start)

### 1. 克隆仓库
```bash
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 设置环境变量
```bash
export BOT_TOKEN="your_telegram_bot_token"
```

### 4. 运行机器人
```bash
python bot.py
```

## 部署 (Deployment)

详细的部署说明请参见 [DEPLOYMENT.md](DEPLOYMENT.md)

支持的部署方式：
- 本地运行
- Heroku
- Docker

## 项目结构 (Project Structure)

```
my-robot/
├── bot.py              # 主程序文件
├── requirements.txt    # Python 依赖
├── Procfile           # Heroku 部署配置
├── .gitignore         # Git 忽略文件
├── README.md          # 项目说明
└── DEPLOYMENT.md      # 部署指南
```

## 环境变量 (Environment Variables)

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `BOT_TOKEN` | Telegram Bot Token (从 @BotFather 获取) | 是 |

## 开发 (Development)

### 代码风格
- 使用 Python 3.8+ 的异步特性
- 遵循 aiogram 3.x 最佳实践

### 测试
```bash
# 语法检查
python -m py_compile bot.py

# 验证导入
python -c "from bot import *"
```

## 更新日志 (Changelog)

### v2.0.0 - 2025-11-05
- ✨ 迁移到 aiogram 3.x API
- 🔒 移除硬编码的 Token，改用环境变量
- 📝 添加完整的部署文档
- 🐛 修复 ImportError: cannot import name 'executor'

### v1.0.0
- 初始版本（使用 aiogram 2.x）

## 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！

## 许可证 (License)

本项目采用 MIT 许可证。

## 联系方式 (Contact)

如有问题，请在 GitHub 上提交 Issue。
