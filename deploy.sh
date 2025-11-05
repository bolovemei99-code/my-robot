#!/bin/bash

# Heroku 部署脚本
# Quick Heroku deployment script

echo "🚀 开始部署到 Heroku..."
echo "Starting Heroku deployment..."

# 检查是否安装 Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "❌ 错误：未找到 Heroku CLI"
    echo "请访问 https://devcenter.heroku.com/articles/heroku-cli 安装"
    echo "Error: Heroku CLI not found"
    echo "Please install from https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# 登录检查
echo "📝 检查 Heroku 登录状态..."
if ! heroku auth:whoami &> /dev/null; then
    echo "请先登录 Heroku..."
    heroku login
fi

# 获取应用名称
read -p "请输入 Heroku 应用名称（留空则自动生成）: " APP_NAME

# 创建或使用现有应用
if [ -z "$APP_NAME" ]; then
    echo "创建新应用..."
    heroku create
else
    # 检查应用是否存在
    if heroku apps:info -a "$APP_NAME" &> /dev/null; then
        echo "使用现有应用: $APP_NAME"
        heroku git:remote -a "$APP_NAME"
    else
        echo "创建新应用: $APP_NAME"
        heroku create "$APP_NAME"
    fi
fi

# 推送代码
echo "📦 推送代码到 Heroku..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
git push heroku "$CURRENT_BRANCH:main" -f

# 启动 worker
echo "⚙️  启动 worker..."
heroku ps:scale worker=1

# 显示日志
echo "✅ 部署完成！"
echo "📊 查看日志："
heroku logs --tail
