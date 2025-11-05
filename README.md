# Telegram Bot - 群转发 + 记账机器人

这是一个Telegram机器人，提供以下功能：
1. 私聊消息转发到所有群
2. 群内简易记账（支持小数）
3. 账单查询

## 部署说明

### 前提条件
- Python 3.11 或更高版本
- Telegram Bot Token（从 @BotFather 获取）

### 本地运行

1. 克隆仓库：
```bash
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行机器人：
```bash
python bot.py
```

### Railway 部署（推荐）

Railway 是一个现代化的云平台，支持自动部署和持续集成。

#### 方法一：通过 GitHub 连接（推荐）

1. 访问 [Railway.app](https://railway.app/) 并登录
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择 `bolovemei99-code/my-robot` 仓库
4. Railway 会自动检测配置并开始部署
5. 部署完成后，机器人会自动运行

**优势**：
- ✅ 自动部署：每次推送到 main 分支都会自动重新部署
- ✅ 免费额度：每月 $5 的免费使用额度
- ✅ 持久化存储：数据文件会保留

#### 方法二：使用 Railway CLI

1. 安装 Railway CLI：
```bash
npm install -g @railway/cli
```

2. 登录：
```bash
railway login
```

3. 初始化项目：
```bash
railway init
```

4. 部署：
```bash
railway up
```

### Heroku 部署

1. 创建 Heroku 应用：
```bash
heroku create your-app-name
```

2. 推送代码：
```bash
git push heroku main
```

3. 启动 worker：
```bash
heroku ps:scale worker=1
```

4. 查看日志：
```bash
heroku logs --tail
```

### 其他平台部署

本项目包含以下文件以支持各种部署平台：
- `railway.json` - Railway 配置文件
- `Procfile` - Heroku/Railway 等平台的进程配置
- `requirements.txt` - Python 依赖
- `runtime.txt` - Python 版本指定

## 使用方法

1. **私聊机器人** - 发送任何消息，机器人会转发到所有已加入的群
2. **群内记账**：
   - `+100` 或 `+100.5 备注` - 入账
   - `-50` 或 `-87.6 备注` - 出账
3. **查看账单** - 在群里发送 `账单` 查看记录

## 文件说明

- `bot.py` - 主程序
- `groups.json` - 群列表存储（自动生成）
- `ledger.json` - 账本数据（自动生成）
- `railway.json` - Railway 配置文件
- `Procfile` - 部署配置
- `requirements.txt` - 依赖列表
- `runtime.txt` - Python 版本
