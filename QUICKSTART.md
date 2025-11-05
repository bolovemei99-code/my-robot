# 快速开始 / Quick Start

## 🚀 3分钟部署指南 / 3-Minute Deployment Guide

### 选项 1: Heroku（推荐）

```bash
# 1. 安装 Heroku CLI
# 访问: https://devcenter.heroku.com/articles/heroku-cli

# 2. 运行一键部署脚本
./deploy.sh

# 3. 设置环境变量（可选，提高安全性）
heroku config:set BOT_TOKEN=你的token

# 完成！🎉
```

### 选项 2: Railway（最简单）

1. 访问 [Railway.app](https://railway.app)
2. 连接 GitHub 账号
3. 选择此仓库
4. 点击 Deploy
5. 完成！🎉

### 选项 3: Render

1. 访问 [Render.com](https://render.com)
2. 创建新的 Web Service
3. 连接此 GitHub 仓库
4. 构建命令: `pip install -r requirements.txt`
5. 启动命令: `python bot.py`
6. 完成！🎉

### 选项 4: VPS / 云服务器

```bash
# 克隆代码
git clone https://github.com/bolovemei99-code/my-robot.git
cd my-robot

# 安装依赖
pip3 install -r requirements.txt

# 后台运行
nohup python3 bot.py > bot.log 2>&1 &

# 或使用 screen
screen -S telegram-bot
python3 bot.py
# 按 Ctrl+A+D 退出
```

## 📱 如何使用机器人 / How to Use

### 1. 添加到群聊
- 将机器人添加到你的 Telegram 群组
- 机器人会自动记录群信息

### 2. 记账功能
```
+100        # 收入 100
-50         # 支出 50
+87.6       # 收入 87.6（支持小数）
+100 工资   # 收入 100，备注"工资"
账单         # 查看账本
```

### 3. 群消息转发
- 私聊机器人发送任何消息
- 消息会自动转发到所有群

### 4. 查看帮助
```
/start      # 查看使用说明
```

## 🔧 故障排查 / Troubleshooting

### 问题: 机器人无响应
**解决方案**:
1. 检查 BOT_TOKEN 是否正确
2. 检查机器人是否在运行: `heroku ps` 或查看日志
3. 确保机器人有群组权限

### 问题: 部署失败
**解决方案**:
1. 检查 Python 版本是否为 3.12+
2. 确保 requirements.txt 正确
3. 查看部署日志获取详细错误

### 问题: 记账不工作
**解决方案**:
1. 确保格式正确: `+数字` 或 `-数字`
2. 支持小数: `+100.5` 或 `-87.6`
3. 可以添加备注: `+100 工资`

## 📞 获取帮助 / Get Help

- 查看完整文档: [README.md](README.md)
- 部署详情: [DEPLOYMENT.md](DEPLOYMENT.md)
- GitHub Issues: 提交问题和建议

## ✅ 检查清单 / Checklist

在部署前确保:
- [ ] 已获取 Telegram Bot Token（从 @BotFather）
- [ ] 已安装必要工具（Heroku CLI / Git）
- [ ] 已克隆或下载代码
- [ ] 已阅读 README.md

部署后确认:
- [ ] 机器人在线（Telegram 搜索机器人用户名）
- [ ] 发送 /start 有响应
- [ ] 已添加到测试群
- [ ] 记账功能正常
- [ ] 消息转发正常

---
**准备好了吗？开始部署吧！** 🚀
**Ready? Let's deploy!** 🚀
