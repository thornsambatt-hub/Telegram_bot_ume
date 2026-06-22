# main.py
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
    # Initialize app with post_init hook
    app = ApplicationBuilder().token(config.BOT_TOKEN).post_init(set_commands).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(button_router))

    if config.WEBHOOK_URL:
        # --- WEBHOOK CONFIGURATION ---
        render_port = int(os.getenv("PORT", 8000))

        print(f"🚀 Starting Webhook Server on port {render_port}...")

        # Clean the URL to ensure it doesn't end with a slash
        clean_url = config.WEBHOOK_URL.rstrip('/')

        app.run_webhook(
            listen="0.0.0.0",
            url_path="webhook",
            webhook_url=f"{clean_url}/webhook"
        )
    else:
        print("🚀 Starting bot in polling mode because WEBHOOK_URL is not set...")
        app.run_polling()

if __name__ == '__main__':
    main()