# 功能详细说明 / Feature Documentation

## 1. 自动回复功能 / Auto Reply

### 智能响应
机器人会自动识别并响应以下类型的消息：

- **数字识别**：直接发送数字（如 `100` 或 `10.5`）会自动记账
- **关键词触发**：设置的快捷回复触发词
- **问候语**：识别"你好"、"hi"、"hello"等问候语
- **感谢语**：识别"谢谢"、"thanks"等感谢语
- **问题识别**：包含"?"或"吗"的问题会引导使用/ask命令

### 使用示例
```
用户: 100
机器人: ✅ 自动记账: 100 | 11-10 14:30

用户: 你好
机器人: 你好 张三！有什么可以帮助你的吗？
发送 /menu 查看功能
```

## 2. 快捷回复系统 / Quick Reply

### 设置快捷回复
```bash
/setquick 触发词 回复内容
```

### 查看所有快捷回复
```bash
/getquick
```

### 删除快捷回复
```bash
/delquick 触发词
```

### 使用示例
```bash
# 设置快捷回复
/setquick 价格 我们的产品价格是 $99

# 当用户发送包含"价格"的消息时
用户: 请问价格多少？
机器人: 我们的产品价格是 $99
```

## 3. Telegram 菜单系统 / Bot Menu

### 主菜单
发送 `/start` 或 `/menu` 显示交互式菜单：

- 📊 记账
- 💬 快捷回复
- 🌐 API服务
- 👥 群管理
- ❓ 帮助

### 命令菜单
机器人会自动注册Telegram命令菜单，用户可以：
1. 点击输入框旁边的菜单按钮
2. 选择想要的命令
3. 快速发送命令

## 4. 第三方API整合 / Third-party API Integration

### 天气查询 🌤
```bash
/weather 城市名
```

示例：
```bash
/weather 北京
# 返回：
🌤 北京 天气
🌡 温度: 15°C
☁️ 状况: 晴
💧 湿度: 60%
```

需要配置 `WEATHER_API_KEY`（OpenWeatherMap API）

### 新闻获取 📰
```bash
/news
```

返回最新的5条科技新闻标题。

需要配置 `NEWS_API_KEY`（NewsAPI）

### ChatGPT 问答 🤖
```bash
/ask 你的问题
```

示例：
```bash
/ask 什么是人工智能？
# 返回：
💭 ChatGPT回答：
人工智能（AI）是计算机科学的一个分支...
```

需要配置 `OPENAI_API_KEY`

## 5. 群发消息功能 / Mass Messaging

### 权限要求
仅限超级管理员（在 `ADMIN_IDS` 环境变量中配置的用户）

### 使用方法
```bash
/mass 用户ID1,用户ID2,用户ID3 消息内容
```

### 示例
```bash
/mass 123456789,987654321 重要通知：系统将于明天维护

# 返回：
📬 群发完成: 2/2
```

## 6. 数据库支持 / Database Support

### 数据库表结构

#### accounts（记账表）
- `user_id`: 用户ID
- `amount`: 金额
- `desc`: 描述
- `time`: 时间

#### users（用户表）
- `user_id`: 用户ID（主键）
- `username`: 用户名
- `first_name`: 名
- `last_name`: 姓
- `join_date`: 加入日期
- `is_banned`: 是否被封禁

#### groups（群组表）
- `group_id`: 群组ID（主键）
- `group_name`: 群组名
- `join_date`: 加入日期
- `welcome_enabled`: 是否启用欢迎消息

#### message_log（消息日志表）
- `id`: 自增ID
- `user_id`: 用户ID
- `chat_id`: 聊天ID
- `message`: 消息内容
- `timestamp`: 时间戳

#### scheduled_messages（定时消息表）
- `id`: 自增ID
- `chat_id`: 聊天ID
- `message`: 消息内容
- `schedule_time`: 计划时间
- `repeat_interval`: 重复间隔
- `enabled`: 是否启用

## 7. 群聊管理功能 / Group Management

### 踢出用户
```bash
# 回复要踢出的用户消息
/kick

# 或指定用户ID
/kick 123456789
```

### 封禁用户
```bash
/ban
# 或
/ban 123456789
```

### 解封用户
```bash
/unban
# 或
/unban 123456789
```

### 禁言用户（1小时）
```bash
/mute
# 或
/mute 123456789
```

### 警告用户
```bash
/warn
# 或
/warn 123456789
```

### 设置欢迎消息模板
```bash
/template 欢迎 {name} 加入我们的群组！
```

模板变量：
- `{name}`: 新成员的名字

### 欢迎新成员
当新成员加入群组时，机器人会：
1. 自动保存用户信息到数据库
2. 发送欢迎消息（使用设置的模板）
3. 显示群规按钮（可点击查看）

## 8. 记账功能 / Accounting

### 添加收入
```bash
/add 金额 描述
```

示例：`/add 1000 工资`

### 添加支出
```bash
/sub 金额 描述
```

示例：`/sub 50 午餐`

### 查询余额
```bash
/balance
```

显示：
- 当前余额
- 最近5条记录（包含时间和描述）

### 快速记账
直接发送数字自动记账：
```
100
# 自动记录为收入
```

## 9. 权限系统 / Permission System

### 超级管理员
在 `.env` 文件中配置：
```bash
ADMIN_IDS=123456789,987654321
```

超级管理员可以：
- 使用所有功能
- 群发消息
- 在任何群组使用管理命令

### 群组管理员
由 Telegram 群组设置决定，群组管理员可以：
- 踢人、封禁、禁言
- 设置欢迎消息模板
- 管理群组设置

### 普通用户
可以使用：
- 记账功能
- 快捷回复
- API查询（天气、新闻、ChatGPT）
- 查看菜单和帮助

## 10. 环境变量配置 / Environment Variables

### 必需配置
- `BOT_TOKEN`: Telegram Bot Token（从 @BotFather 获取）

### 可选配置
- `ADMIN_IDS`: 超级管理员ID列表（逗号分隔）
- `WEATHER_API_KEY`: OpenWeatherMap API Key
- `NEWS_API_KEY`: NewsAPI Key
- `OPENAI_API_KEY`: OpenAI API Key
- `RAILWAY_STATIC_URL`: 部署域名
- `PORT`: 服务器端口（默认5000）

### 配置方法
1. 复制 `.env.example` 为 `.env`
2. 填入实际的配置值
3. 重启机器人

## 11. 部署说明 / Deployment

### Railway 部署
1. 连接 GitHub 仓库
2. 在 Railway 设置环境变量
3. 自动部署

### 本地运行
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export BOT_TOKEN="your_token"

# 运行
python main.py
```

### Docker 部署（可选）
```bash
# 构建镜像
docker build -t telegram-bot .

# 运行容器
docker run -d --env-file .env telegram-bot
```

## 12. 安全建议 / Security Tips

1. ✅ 不要将 `.env` 文件提交到 Git
2. ✅ 定期更换 API Keys
3. ✅ 限制超级管理员数量
4. ✅ 定期备份数据库
5. ✅ 监控异常登录和操作
6. ✅ 使用 HTTPS webhook

## 13. 常见问题 / FAQ

### Q: 如何获取 Telegram Bot Token？
A: 在 Telegram 中搜索 @BotFather，发送 `/newbot` 创建新机器人。

### Q: 如何找到我的用户ID？
A: 在 Telegram 中搜索 @userinfobot，发送任意消息获取你的ID。

### Q: API Keys 在哪里获取？
A: 
- Weather: https://openweathermap.org/api
- News: https://newsapi.org/
- OpenAI: https://platform.openai.com/

### Q: 数据库文件在哪里？
A: `data.db` 文件会在首次运行时自动创建在项目目录中。

### Q: 如何备份数据？
A: 复制 `data.db` 和 `quick.json` 文件即可。

## 14. 技术栈 / Tech Stack

- **Python 3.7+**
- **pyTelegramBotAPI**: Telegram Bot API 封装
- **Flask**: Web 框架（Webhook）
- **SQLite3**: 数据库
- **Requests**: HTTP 请求库

## 15. 贡献指南 / Contributing

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 支持 / Support

如有问题，请：
1. 查看本文档
2. 搜索已有 Issues
3. 创建新 Issue
