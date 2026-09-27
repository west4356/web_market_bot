import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Telegram Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN", "8829323588:AAEm3sgZK47awtnMNoUexvwdbcDmpeWAMPk")

# Admin IDs (Telegram User IDs who receive order alerts and can manage orders)
ADMIN_IDS = [
    # Add your Telegram numeric user ID here (e.g. 123456789)
]

# Dedicated Channel for Orders (e.g. "@YourOrdersChannel" or "-100xxxxxxxxxx")
ORDERS_CHANNEL_ID = os.getenv("ORDERS_CHANNEL_ID", "")

# Web Server Configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", "8080"))

# Database
DB_PATH = str(BASE_DIR / "market.db")

# Public WebApp URL (supports auto-detection on Render.com, Railway, etc.)
WEBAPP_URL = os.getenv("WEBAPP_URL") or os.getenv("RENDER_EXTERNAL_URL", "")

# Crypto Wallets for Payment
CRYPTO_CONFIG = {
    "TON": {
        "address": "UQDC7q9w2Z0r8GvKxY9_EXAMPLE_TON_WALLET_ADDRESS",
        "network": "The Open Network (TON)",
        "symbol": "TON",
        "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data="
    },
    "USDT": {
        "address": "TYx123456789_EXAMPLE_USDT_TRC20_WALLET_ADDRESS",
        "network": "TRON (TRC-20) / TON USDT",
        "symbol": "USDT",
        "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data="
    }
}

# Bank / Card info (optional for manual payment)
CARD_CONFIG = {
    "card_number": "8600 0000 0000 0000",
    "bank_name": "Visa / MasterCard / National Bank",
    "holder_name": "MARKET STORE"
}
