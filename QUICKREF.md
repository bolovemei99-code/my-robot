# 快速参考 / Quick Reference

## 🚀 快速开始 / Quick Start

### 1. 获取 Bot Token
访问 Telegram，搜索 [@BotFather](https://t.me/BotFather)
```
/newbot
# 按提示创建机器人
# 保存获得的 Token
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入 BOT_TOKEN
```

### 3. 本地运行
```bash
pip install -r requirements.txt
python main.py
```

### 4. 部署到 Railway
1. Fork 本仓库
2. 访问 [Railway](https://railway.app)
3. 导入 GitHub 仓库
4. 设置环境变量 `BOT_TOKEN`
5. 自动部署完成

## 📋 常用命令速查 / Command Cheat Sheet

### 基础 / Basic
```
/start   - 开始使用
/menu    - 功能菜单
/help    - 帮助信息
```

### 记账 / Accounting
```
100              - 快速记账
/add 100 工资    - 添加收入
/sub 50 午餐     - 添加支出
/balance         - 查询余额
```

### 快捷回复 / Quick Reply
```
/setquick hi 你好  - 设置
/getquick          - 查看
/delquick hi       - 删除
```

### API服务 / API
```
/weather 北京              - 天气
/news                      - 新闻
/ask 什么是人工智能？      - ChatGPT
```

### 群管理 / Group (管理员)
```
/kick    - 踢人 (回复消息)
/ban     - 封禁
/unban   - 解封
/mute    - 禁言1小时
/warn    - 警告
/template 欢迎 {name}  - 设置欢迎语
```

### 超级管理员 / Super Admin
```
/mass 123,456 通知内容  - 群发消息
```

## 🔧 环境变量 / Environment Variables

### 必需 / Required
```bash
BOT_TOKEN=your_telegram_bot_token
```

### 可选 / Optional
```bash
ADMIN_IDS=123456789,987654321
WEATHER_API_KEY=your_key
NEWS_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## 🗄️ 数据库表 / Database Tables

| 表名 | 用途 |
|------|------|
| accounts | 记账数据 |
| users | 用户信息 |
| groups | 群组信息 |
| message_log | 消息日志 |
| scheduled_messages | 定时消息 |

## 📁 项目文件 / Project Files

| 文件 | 说明 |
|------|------|
| main.py | 主程序 (676行) |
| README.md | 项目文档 |
| FEATURES.md | 功能详解 |
| requirements.txt | 依赖包 |
| .env.example | 配置模板 |
| .gitignore | Git忽略 |
| LICENSE | MIT许可证 |

## 🔐 安全提示 / Security Tips

✅ **必做:**
- 不要泄露 BOT_TOKEN
- 使用环境变量
- 定期备份 data.db
- 限制管理员权限

❌ **禁止:**
- 提交 .env 到 Git
- 公开分享 Token
- 使用弱密码

## 🐛 故障排查 / Troubleshooting

### 机器人无响应
1. 检查 BOT_TOKEN 是否正确
2. 检查 Webhook 是否设置成功
3. 查看日志输出

### API 功能不工作
1. 检查 API Key 是否配置
2. 验证 API Key 是否有效
3. 检查网络连接

### 数据库错误
1. 删除 data.db 重新初始化
2. 检查文件权限
3. 备份后重新运行

## 📞 获取帮助 / Get Help

- 📖 阅读 [README.md](README.md)
- 📚 查看 [FEATURES.md](FEATURES.md)
- 🐛 提交 [Issue](https://github.com/bolovemei99-code/my-robot/issues)
- 💬 参与讨论

## 🎯 下一步 / Next Steps

1. ⚙️ 配置环境变量
2. 🚀 部署机器人
3. 🤖 从 BotFather 获取 Token
4. ✅ 测试所有功能
5. 📱 邀请机器人到群组
6. 🎉 开始使用！

---

**项目地址**: https://github.com/bolovemei99-code/my-robot
**许可证**: MIT License
