# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Render provides the PORT variable automatically. Default to 8000 locally.
PORT = int(os.getenv("PORT", 8000))
# Your public web URL given by Render (e.g., https://my-bot.onrender.com)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    raise ValueError("❌ CRITICAL ERROR: TELEGRAM_BOT_TOKEN is missing!")