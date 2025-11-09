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
