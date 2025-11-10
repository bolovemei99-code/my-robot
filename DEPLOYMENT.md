# MCP Bot Deployment Guide

## 📋 Project Structure
```
my-robot/
├── main.py              # Bot application with /mcp command
├── mcp.json            # MCP server configuration
├── requirements.txt    # Python dependencies
├── Procfile           # Railway deployment config
└── .gitignore         # Excluded files
```

## 🚀 Railway Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Add MCP configuration"
git push origin main
```

### 2. Deploy to Railway
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `my-robot` repository
4. Railway will auto-detect the Procfile

### 3. Set Environment Variables
In Railway Dashboard → Settings → Variables, add:

| Key | Value | Required |
|-----|-------|----------|
| `TG_TOKEN` | Your Telegram Bot Token | ✅ Yes |
| `XAI_API_KEY` | xAI API Key (for Grok) | ⚪ Optional |
| `OPENAI_API_KEY` | OpenAI API Key | ⚪ Optional |

### 4. Generate Domain
1. Go to Settings → Networking
2. Click "Generate Domain"
3. Copy the generated URL (e.g., `your-bot.up.railway.app`)

### 5. Set Telegram Webhook
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://your-bot.up.railway.app/webhook"
```

Replace `<YOUR_TOKEN>` with your actual Telegram bot token.

## 🧪 Testing

### Test Commands
1. Private message your bot:
   ```
   /help
   ```
   Should show: "🎉 命令: /mcp 你好 (AI对话) /add 10 午饭..."

2. Test MCP AI chat:
   ```
   /mcp 你好
   ```
   Should reply with AI response

3. Test other features:
   ```
   /add 10 午饭
   /balance
   ```

## 🔧 MCP Configuration

### Supported Models (mcp.json)
1. **local-llm** - Llama3 via Ollama
   - Requires Ollama running on localhost:11434
   - Uses MCP server with Python

2. **grok-api** - xAI Grok
   - Requires XAI_API_KEY environment variable
   - API: https://api.x.ai/v1/chat/completions

3. **openai-proxy** - OpenAI GPT
   - Requires OPENAI_API_KEY environment variable
   - API: https://api.openai.com/v1/chat/completions

## 📊 Architecture

```
Telegram User
    ↓
Telegram API (webhook)
    ↓
Railway (Flask app on port 8080)
    ↓
/mcp command handler
    ↓
MCP Server (localhost:8000)
    ↓
AI Model (Llama3/Grok/OpenAI)
```

## 🛠️ Troubleshooting

### Bot not responding
- Check Railway logs for errors
- Verify TG_TOKEN is set correctly
- Confirm webhook is set: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`

### MCP errors
- Ensure mcp-server is running (Railway Procfile handles this)
- Check if localhost:8000 is accessible
- Verify API keys for external models

### Deployment fails
- Check requirements.txt has all dependencies
- Verify Procfile syntax is correct
- Check Railway build logs

## 📝 Key Changes from Original

1. ✅ Fixed JSON syntax in mcp.json (quotes and spelling)
2. ✅ Changed TOKEN from hardcoded to environment variable
3. ✅ Added Flask app.run() for proper server startup
4. ✅ Added /mcp command handler for AI chat
5. ✅ Updated requirements.txt with Flask, mcp-server, requests

## 🎉 Success Criteria

When deployment is successful, you should:
- ✅ See "MCP Bot 启动！" in Railway logs
- ✅ Receive responses from `/help` command
- ✅ Get AI responses from `/mcp 你好` command
- ✅ Have 2 processes running in Railway (web + mcp)

---

**Need help?** Check Railway logs or Telegram bot responses for error messages.
