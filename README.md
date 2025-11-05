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
- `Procfile` - 部署配置
- `requirements.txt` - 依赖列表
- `runtime.txt` - Python 版本
