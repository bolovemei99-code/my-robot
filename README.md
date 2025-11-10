# Telegram Bot with API Security Scanning

A Telegram bot with Flask web server and integrated Mayhem for API security scanning.

## Features

- Telegram bot with webhook support
- Flask API with OpenAPI specification
- Health check endpoint
- Automated API security scanning with Mayhem for API

## Setup

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (required for production)
- `RAILWAY_STATIC_URL`: Railway deployment URL (optional, for webhook setup)
- `PORT`: Server port (default: 8080)
- `MAYHEM_TOKEN`: Mayhem API token (required for GitHub Actions security scanning)

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8080`

### API Endpoints

- `GET /health` - Health check endpoint
- `GET /openapi.json` - OpenAPI specification
- `POST /webhook` - Telegram webhook endpoint

## GitHub Actions Security Scanning

This repository uses Mayhem for API to perform automated security scanning. To enable it:

1. Create a Mayhem account at https://app.mayhem.security
2. Create an API token at https://app.mayhem.security/-/settings/user/api-tokens
3. Add the API token as a GitHub secret named `MAYHEM_TOKEN` in your repository settings:
   - Go to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name: `MAYHEM_TOKEN`
   - Value: Your Mayhem API token
   - Click "Add secret"

The security scan will run automatically on push and pull requests to the main branch.

## Running Tests

The API can be tested using the startup script:

```bash
./run_your_api.sh
```

This will:
1. Install dependencies
2. Start the Flask server
3. Wait for the API to be ready
4. Verify the health endpoint is responding
