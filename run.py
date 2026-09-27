import asyncio
import logging
import sys
import os

# Fix Windows console encoding for UTF-8 / emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import uvicorn
from pathlib import Path

import config
import database
import bot_service
from server import app
from tunnel import CloudflareTunnel

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("market_runner")

async def main():
    print("=" * 60)
    print("🚀  STARTING TELEGRAM WEB APP MARKET")
    print("=" * 60)

    # 1. Initialize SQLite Database
    logger.info("Initializing SQLite database...")
    database.init_db()
    logger.info("Database ready at %s", config.DB_PATH)

    # 2. Start Cloudflare HTTPS Tunnel
    tunnel = None
    if not config.WEBAPP_URL:
        logger.info("Starting Cloudflare tunnel to obtain public HTTPS URL for Telegram...")
        tunnel = CloudflareTunnel(port=config.SERVER_PORT)
        try:
            public_url = tunnel.start(timeout=25)
            if public_url:
                config.WEBAPP_URL = public_url
                print("\n" + "*" * 60)
                print(f"🌐  PUBLIC HTTPS WEB APP URL: {public_url}")
                print("*" * 60 + "\n")
            else:
                logger.warning("Cloudflare tunnel timed out. Using localhost fallback.")
        except Exception as e:
            logger.error(f"Failed to start Cloudflare tunnel: {e}")
    else:
        print(f"Using pre-configured WebApp URL: {config.WEBAPP_URL}")

    # 3. Setup Telegram Bot Application
    logger.info("Initializing Telegram Bot (@vst_starsmarket_bot)...")
    bot_app = bot_service.setup_application()
    
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling(drop_pending_updates=True)
    logger.info("Telegram Bot polling started successfully!")

    # 4. Configure Bot Menu Button with the HTTPS URL
    if config.WEBAPP_URL and config.WEBAPP_URL.startswith("https://"):
        try:
            await bot_service.set_menu_button(config.WEBAPP_URL)
            logger.info("Telegram Chat Menu Button configured with WebApp URL!")
        except Exception as e:
            logger.warning(f"Could not set menu button: {e}")

    # 5. Start Uvicorn Web Server
    uv_config = uvicorn.Config(
        app=app,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        log_level="info",
        access_log=False
    )
    uv_server = uvicorn.Server(uv_config)
    server_task = asyncio.create_task(uv_server.serve())

    print("\n" + "=" * 60)
    print("✨  TELEGRAM MARKET APP IS LIVE AND READY!")
    print(f"🤖  Bot Username: @vst_starsmarket_bot")
    if config.WEBAPP_URL:
        print(f"📱  Web App URL: {config.WEBAPP_URL}")
        print(f"🔗  Direct Telegram Link: https://t.me/vst_starsmarket_bot")
    print(f"💻  Local API Server: http://{config.SERVER_HOST}:{config.SERVER_PORT}")
    print("=" * 60 + "\n")

    try:
        # Keep running until interrupted
        await server_task
    except (asyncio.CancelledError, KeyboardInterrupt):
        logger.info("Shutdown signal received.")
    finally:
        logger.info("Shutting down bot and server...")
        uv_server.should_exit = True
        try:
            await bot_app.updater.stop()
            await bot_app.stop()
            await bot_app.shutdown()
        except Exception:
            pass
        if tunnel:
            tunnel.stop()
        logger.info("Clean shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting Telegram Market App.")
        sys.exit(0)
