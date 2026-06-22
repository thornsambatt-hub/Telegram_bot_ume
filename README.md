<<<<<<< HEAD
# Telegram_bot_ume
=======
# UME Kratié Telegram Bot

## Setup

1. Create a virtual environment.
	- PowerShell: `.venv\Scripts\Activate.ps1`
2. Install dependencies.
	- `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your values.

## Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your BotFather token.
- `WEBHOOK_URL`: Your public HTTPS URL for deployment.
- `PORT`: Optional local port override. Defaults to `8000`.

## Run Locally

If `WEBHOOK_URL` is not set, the bot starts in polling mode:

```powershell
python main.py
```

## Deploy

When `WEBHOOK_URL` is set, the bot uses webhook mode and listens on the configured `PORT`.
>>>>>>> 0c1462a (Finnish Hosting1)
