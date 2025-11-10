# My Robot - Telegram Bot

一个功能强大的 Telegram 机器人，支持记账、群管理、快捷回复等功能。

A powerful Telegram bot with accounting, group management, and quick reply features.

## 功能特性 / Features

### 📊 记账功能 / Accounting
- 自动识别金额并记账
- 支持添加收入和支出
- 查询账户余额
- 记录交易描述和时间

### 👥 群管理 / Group Management
- 踢出群成员 (`/kick`)
- 封禁用户 (`/ban`)
- 管理员权限验证
- 新成员欢迎消息

### 💬 快捷回复 / Quick Reply
- 自定义触发词和回复
- 设置欢迎消息模板
- 支持变量替换（如 `{name}`）

### 📢 群发消息 / Mass Messaging
- 批量发送消息给指定用户
- 管理员专用功能

## 安装部署 / Installation

### 环境要求 / Requirements
- Python 3.7+
- SQLite3

### 安装步骤 / Setup

1. 克隆仓库 / Clone the repository:
```bash
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot
```

2. 安装依赖 / Install dependencies:
```bash
pip install -r requirements.txt
```

3. 配置环境变量 / Configure environment variables:
```bash
export BOT_TOKEN="your_telegram_bot_token"
export RAILWAY_STATIC_URL="your_webhook_url"
```

4. 运行机器人 / Run the bot:
```bash
python main.py
```

## 命令列表 / Commands

| 命令 / Command | 说明 / Description | 示例 / Example |
|----------------|-------------------|----------------|
| `/add <金额> <描述>` | 添加收入 / Add income | `/add 100 工资` |
| `/sub <金额> <描述>` | 添加支出 / Add expense | `/sub 50 午餐` |
| `/balance` | 查询余额 / Check balance | `/balance` |
| `/setquick <触发词> <回复>` | 设置快捷回复 / Set quick reply | `/setquick hi 你好` |
| `/getquick` | 查看所有快捷回复 / View all quick replies | `/getquick` |
| `/template <模板>` | 设置欢迎模板 / Set welcome template | `/template 欢迎 {name}` |
| `/kick` | 踢出用户 / Kick user | `/kick` (回复消息) |
| `/ban` | 封禁用户 / Ban user | `/ban` (回复消息) |
| `/mass <用户ID...> <消息>` | 群发消息 / Mass message | `/mass 123 456 通知` |
| `/help` | 显示帮助 / Show help | `/help` |

## 自动记账 / Auto Accounting

直接发送数字即可自动记账：
Simply send a number to automatically record it:

```
10.5
```
机器人会自动记录为收入。/ Bot will automatically record it as income.

## 配置文件 / Configuration Files

- `main.py` - 主程序 / Main bot program
- `requirements.txt` - Python 依赖 / Python dependencies
- `Procfile` - 部署配置 / Deployment configuration
- `mcp.json` - MCP 服务器配置 / MCP server configuration
- `data.db` - SQLite 数据库 / SQLite database (auto-created)
- `quick.json` - 快捷回复数据 / Quick reply data (auto-created)

## 部署 / Deployment

### Railway 部署 / Railway Deployment

1. 连接 GitHub 仓库到 Railway
2. 设置环境变量：
   - `BOT_TOKEN`: 你的 Telegram Bot Token
   - `RAILWAY_STATIC_URL`: Railway 提供的域名
3. Railway 会自动使用 Procfile 启动服务

### 其他平台 / Other Platforms

确保设置正确的 Webhook URL 并配置环境变量。
Make sure to set the correct Webhook URL and configure environment variables.

## 数据库结构 / Database Structure

### accounts 表 / accounts table
- `user_id` - 用户 ID / User ID
- `amount` - 金额 / Amount
- `desc` - 描述 / Description
- `time` - 时间 / Time

### quick 表 / quick table
- `trigger` - 触发词 / Trigger word
- `response` - 回复内容 / Response text

## 安全提示 / Security Notes

⚠️ **重要 / Important**: 
- 不要将 Bot Token 提交到代码仓库 / Never commit Bot Token to the repository
- 使用环境变量存储敏感信息 / Use environment variables for sensitive data
- 定期备份数据库 / Regularly backup the database

## 开发 / Development

### 本地测试 / Local Testing

```bash
# 设置环境变量 / Set environment variables
export BOT_TOKEN="your_token"

# 运行程序 / Run the program
python main.py
```

### 贡献指南 / Contributing

欢迎提交 Issue 和 Pull Request！
Issues and Pull Requests are welcome!

## 许可证 / License

MIT License - 详见 LICENSE 文件 / See LICENSE file for details

## 联系方式 / Contact

如有问题或建议，请提交 Issue。
For questions or suggestions, please submit an Issue.
