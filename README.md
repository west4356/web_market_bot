# 🌟 Telegram Web App Market (Stars, Premium & Gifts)

A production-ready Telegram Mini App (TWA) marketplace for:
1. **Telegram Paid Reactions (Stars)**: Channel & post reaction boost packages (50, 100, 250, 500, 1000, 2500, 5000 Stars, or custom count) with emoji selection (⭐, 🔥, ❤️, 👍, 🚀, 🎉, etc.).
2. **Telegram Premium**: 3, 6, and 12-month gift subscriptions for any Telegram username.
3. **Telegram Collectible Profile Gifts**: Cakes, Stars, Hearts, Rockets, Trophies, Teddy Bears, Diamonds, and Crowns with custom dedication messages and anonymous sender option.
4. **Native Telegram Stars Payments**: 1-click native in-app payment sheet via `openInvoice` and `currency="XTR"`.
5. **TON & USDT Crypto Payments**: QR codes and wallet addresses with payment confirmation.
6. **Order Management & Real-time Alerts**: SQLite storage with instant bot notifications for customers and administrators.

---

## 🤖 Bot Details
- **Bot Name**: WEB Market
- **Bot Username**: `@vst_starsmarket_bot`
- **Bot Link**: [https://t.me/vst_starsmarket_bot](https://t.me/vst_starsmarket_bot)

---

## 📁 Project Structure

```
telegram_market_app/
│
├── config.py             # Bot token, server port, wallet addresses, and settings
├── catalog.py            # Products (Stars Reactions, Premium, Collectible Gifts)
├── database.py           # SQLite database for users, orders, and stats
├── bot_service.py        # Telegram Bot handlers, notifications, and Stars payments
├── server.py             # FastAPI backend with REST API and static file serving
├── tunnel.py             # Cloudflare tunnel manager (creates secure HTTPS URL)
├── run.py                # All-in-one runner script
├── cloudflared.exe       # Cloudflare executable for instant HTTPS tunneling
├── requirements.txt      # Python dependencies
│
└── static/               # Telegram Mini App Frontend
    ├── index.html        # Main HTML layout with responsive tabs and modals
    ├── css/style.css     # Telegram theme variables, dark mode & glassmorphism
    └── js/app.js         # Telegram WebApp SDK, dynamic catalog, checkout & i18n
```

---

## 🚀 How to Run

Run the all-in-one launcher script:

```powershell
python run.py
```

### What happens automatically:
1. The SQLite database is created and initialized at `market.db`.
2. The bundled `cloudflared.exe` starts and generates a live public HTTPS URL (e.g. `https://xxxx.trycloudflare.com`).
3. The Telegram Bot sets its Chat Menu Button to open the Web App URL.
4. The FastAPI web server and Telegram Bot begin listening concurrently.

---

## 📱 How to Use in Telegram

1. Open Telegram and search for `@vst_starsmarket_bot` (or click [t.me/vst_starsmarket_bot](https://t.me/vst_starsmarket_bot)).
2. Tap **/start** or click the **"🛒 Market"** button in the bottom-left corner of the chat.
3. The Mini App opens inside Telegram:
   - Select **Stars Reactions**, paste a channel post link, pick an emoji, and choose a package.
   - Select **Premium**, enter a username, and pick 3, 6, or 12 months.
   - Select **Gifts**, choose a collectible gift (e.g. 🎂 Cake, 🚀 Rocket, 💎 Diamond), add a personal note, and toggle anonymous if desired.
4. Tap **Order / Pay** and choose your preferred payment method:
   - **⭐ Telegram Stars**: Native Telegram 1-click payment sheet opens in Telegram.
   - **💎 TON / USDT**: Copy the wallet address or scan the QR code.
   - **💳 Card**: Transfer details.
5. Track your order status in the **"My Orders"** tab or receive instant status updates in Telegram chat!

---

## 👑 Admin Panel & Orders

- **Inside Telegram**: Run `/admin` in chat with `@vst_starsmarket_bot` to view live revenue, total orders, and click **✅ Mark Done** or **❌ Cancel** to notify the customer automatically.
- **Inside the Web App**: If you are registered as an admin, a 👑 icon appears in the top header with real-time order management.
- To set your Telegram ID as an admin, simply add your ID in `config.py` under `ADMIN_IDS` or send `/start admin_setup` to the bot.
