# main.py
import config
import asyncio
import os
from aiohttp import web
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, Application
from bot.handlers.start import start
from bot.handlers.message import button_router

async def set_commands(application: Application):
    """Registers the bottom Menu button automatically on startup."""
    bot_commands = [
        BotCommand("start", "ចាប់ផ្តើម (Start the bot)"),
        BotCommand("menu", "ព័ត៌មានអំពីសាកលវិទ្យាល័យ (Main Menu)")
    ]
    await application.bot.set_my_commands(bot_commands)

async def amain():
    """Asynchronous main launcher to satisfy Python 3.14 event loops."""

    # Initialize app with post_init hook
    app = ApplicationBuilder().token(config.BOT_TOKEN).post_init(set_commands).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(button_router))

    # --- WEBHOOK CONFIGURATION ---
    if config.WEBHOOK_URL:
        render_port = int(os.getenv("PORT", 8000))
        print(f"🚀 Starting Webhook Server on port {render_port}...")

        clean_url = config.WEBHOOK_URL.strip("/")

        # Initialize the underlying updater infrastructure cleanly
        await app.initialize()
        await app.updater.start_webhook(
            listen="0.0.0.0",
            port=render_port,
            url_path="webhook",
            webhook_url=f"{clean_url}/webhook"
        )

        # Add a small homepage route so cron / health probes receive 200 OK
        try:
            web_app = getattr(app.updater, "web_app", None)
            if web_app is not None:
                async def homepage_handler(request):
                    return web.Response(text="🟢 UME Kratie Portal Bot Server is Live and Active!")

                web_app.router.add_get("/", homepage_handler)
            else:
                # Fallback for older/internal servers that expose an http_server
                http_server = getattr(app.updater, "http_server", None)
                if http_server is not None:
                    async def tornado_homepage(request):
                        from tornado.web import RequestHandler
                        if isinstance(request, RequestHandler):
                            request.write("🟢 UME Kratie Portal Bot Server is Live and Active!")
                            request.finish()

                    http_server.add_handlers(r".*", [(r"/", tornado_homepage)])
        except Exception as e:
            print("Warning: could not add homepage handler:", e)

        await app.start()

        # Keep the web service running continuously in the background
        while True:
            await asyncio.sleep(3600)
    else:
        print("🚀 Starting bot in polling mode because WEBHOOK_URL is not set...")
        # Use simple initializer fallback for local environment testing
        await app.initialize()
        await app.updater.start_polling()
        await app.start()
        while True:
            await asyncio.sleep(3600)

def main():
    if not config.BOT_TOKEN:
        raise ValueError("❌ CRITICAL ERROR: TELEGRAM_BOT_TOKEN is missing!")
        
    # Force Python 3.14 to open a clean asynchronous runner loop
    asyncio.run(amain())

if __name__ == '__main__':
    main()