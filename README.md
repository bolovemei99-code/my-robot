# Telegram 机器人 - 群转发 + 记账

这是一个Telegram机器人，支持群消息转发和简易记账功能。

## 功能

1. **群消息转发**：私聊机器人，消息会转发到机器人所在的所有群
2. **记账功能**：
   - 在群内发送 `+100` 或 `+100.5` 记录收入
   - 在群内发送 `-50` 或 `-87.6` 记录支出
   - 支持添加备注，如 `+100 工资收入`
   - 发送 `账单` 查看当前群的完整账本
3. **自动群管理**：机器人被拉入/移出群时自动更新群列表

## 部署到 Heroku

### 前提条件
- Heroku 账号
- Heroku CLI 工具
- Git

### 部署步骤

1. **登录 Heroku**
```bash
heroku login
```

2. **创建 Heroku 应用**
```bash
heroku create 你的应用名称
```

3. **推送代码**
```bash
git push heroku main
```
或者如果你在分支上：
```bash
git push heroku 你的分支名:main
```

4. **启动 worker**
```bash
heroku ps:scale worker=1
```

5. **查看日志**
```bash
heroku logs --tail
```

### 配置说明

- `bot.py` - 主程序文件
- `requirements.txt` - Python依赖
- `Procfile` - Heroku进程配置（worker类型）

### 其他部署平台

#### Railway
1. 连接 GitHub 仓库
2. 选择此项目
3. Railway 会自动识别 Procfile 和 requirements.txt
4. 部署成功

#### Render
1. 创建新的 Web Service
2. 连接 GitHub 仓库
3. 构建命令：`pip install -r requirements.txt`
4. 启动命令：`python bot.py`

#### VPS (Ubuntu/Debian)
```bash
# 安装依赖
sudo apt update
sudo apt install python3 python3-pip git

# 克隆代码
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot

# 安装Python包
pip3 install -r requirements.txt

# 使用 systemd 或 screen 运行
# 方法1: 直接运行
python3 bot.py

# 方法2: 使用 screen 后台运行
screen -S telegram-bot
python3 bot.py
# Ctrl+A+D 退出screen
```

## 使用说明

### 启动机器人
发送 `/start` 命令给机器人查看使用说明

### 群记账
1. 将机器人拉入群聊
2. 在群内发送：
   - `+100` - 记录收入100
   - `-50` - 记录支出50
   - `+87.6 午餐费用` - 记录收入并添加备注
   - `账单` - 查看账单详情

### 群转发
1. 私聊机器人发送任何消息
2. 消息会自动转发到机器人所在的所有群

## 文件说明

- `groups.json` - 保存机器人所在群列表（运行时自动创建）
- `ledger.json` - 保存各群账本数据（运行时自动创建）

## 技术栈

- Python 3.12+
- aiogram 3.13.1 (Telegram Bot Framework)
- asyncio (异步处理)

## 安全提示

**重要**：强烈建议使用环境变量来保护你的 Bot Token！

本项目已支持环境变量配置。在生产环境中，请设置 `BOT_TOKEN` 环境变量：

Heroku 设置环境变量：
```bash
heroku config:set BOT_TOKEN=你的token
```

Linux/Mac 设置环境变量：
```bash
export BOT_TOKEN="你的token"
python3 bot.py
```

Windows 设置环境变量：
```bash
set BOT_TOKEN=你的token
python bot.py
```

如果不设置环境变量，bot.py 会使用代码中的默认 token（仅用于开发测试）。

## 许可证

MIT License
