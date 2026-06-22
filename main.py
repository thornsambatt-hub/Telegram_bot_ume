# main.py
import asyncio
import os

import config
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, Application
from bot.handlers.start import start
from bot.handlers.message import button_router

async def set_commands(application: Application):
    """Registers the bottom Menu button automatically on startup."""
    bot_commands = [
        BotCommand("start", "ចាប់ផ្តើម"),
        BotCommand("menu", "ព័ត៌មានអំពីសាកលវិទ្យាល័យ")
    ]
    await application.bot.set_my_commands(bot_commands)

def main():
    if not config.WEBHOOK_URL:
        raise ValueError("❌ CRITICAL ERROR: WEBHOOK_URL environment variable is missing!")

    # Initialize app with post_init hook
    app = ApplicationBuilder().token(config.BOT_TOKEN).post_init(set_commands).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(button_router))

    # --- WEBHOOK CONFIGURATION ---
    render_port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting Webhook Server on port {render_port}...")

    # Explicitly create and set an event loop for Python 3.12+ / 3.14
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    # Clean the URL to ensure it doesn't end with a slash
    clean_url = config.WEBHOOK_URL.strip("/")

    app.run_webhook(
        listen="0.0.0.0",
        port=render_port,
        url_path="webhook",
        webhook_url=f"{clean_url}/webhook"
    )

if __name__ == '__main__':
    main()