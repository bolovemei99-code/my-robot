# Telegram 机器人 - Railway 部署指南

这是一个使用 aiogram 构建的 Telegram 机器人，可以轻松部署到 Railway 平台。

## 功能特点

- 响应 `/start` 命令
- 回显用户发送的消息

## Railway 部署步骤

### 1. 准备工作

确保你有：
- 一个 Telegram Bot Token（从 [@BotFather](https://t.me/botfather) 获取）
- 一个 [Railway](https://railway.app) 账户

### 2. 获取 Bot Token

1. 在 Telegram 中找到 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 命令创建新机器人
3. 按照提示设置机器人名称
4. 保存 BotFather 给你的 Token（格式类似：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`）

### 3. 部署到 Railway

#### 方法一：从 GitHub 部署（推荐）

1. 登录 [Railway](https://railway.app)
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择这个仓库
5. Railway 会自动检测到 Python 项目并开始构建

#### 方法二：使用 Railway CLI

```bash
# 安装 Railway CLI
npm i -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 部署
railway up
```

### 4. 配置环境变量

部署后，你需要在 Railway 中设置环境变量：

1. 在 Railway 项目页面，点击你的服务
2. 进入 "Variables" 标签
3. 添加新变量：
   - **变量名**: `BOT_TOKEN`
   - **变量值**: 你从 BotFather 获取的完整 token

4. 保存后，Railway 会自动重启服务

### 5. 验证部署

1. 查看 Railway 的日志，应该看到 "机器人正在启动..." 的消息
2. 在 Telegram 中找到你的机器人
3. 发送 `/start` 命令测试
4. 发送任何消息，机器人应该会回显

## 项目文件说明

- `bot.py` - 机器人主程序
- `requirements.txt` - Python 依赖包
- `Procfile` - Railway 运行配置
- `railway.json` - Railway 部署配置（可选）

## 环境变量

| 变量名 | 说明 | 是否必需 |
|--------|------|----------|
| `BOT_TOKEN` | Telegram Bot Token | 是 |

## 本地开发

如果你想在本地测试：

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export BOT_TOKEN="你的bot_token"

# 运行机器人
python bot.py
```

## 常见问题

### 机器人没有响应？

1. 检查 Railway 日志是否有错误
2. 确认 `BOT_TOKEN` 环境变量已正确设置
3. 确认 token 格式正确（包含冒号和两部分）
4. 检查机器人是否在 BotFather 中被禁用

### 如何更新机器人？

只需推送代码到 GitHub，Railway 会自动重新部署。

### 如何查看日志？

在 Railway 项目页面，点击你的服务，然后查看 "Deployments" 标签下的日志。

## 技术栈

- Python 3.x
- aiogram 3.13.1 (Telegram Bot 框架)
- Railway (部署平台)

## 许可证

本项目遵循 MIT 许可证。

## 支持

如有问题，请在 GitHub 上提出 Issue。
