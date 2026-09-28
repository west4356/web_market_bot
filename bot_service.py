import asyncio
import logging
import html
from telegram import (
    Update,
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    MenuButtonWebApp,
    LabeledPrice
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    ChatMemberHandler,
    ContextTypes,
    filters
)
import config
import database
import catalog

logger = logging.getLogger(__name__)

# Global bot application instance
bot_app = None

def get_bot_instance() -> Bot:
    """Returns the active bot instance or a fresh Bot client using BOT_TOKEN."""
    if bot_app and bot_app.bot:
        return bot_app.bot
    return Bot(token=config.BOT_TOKEN)

async def set_menu_button(web_app_url: str):
    """Configures the default Telegram bottom-left Menu Button to open the Web App."""
    bot = get_bot_instance()
    try:
        if web_app_url and web_app_url.startswith("https://"):
            await bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(text="🛒 Market", web_app=WebAppInfo(url=web_app_url))
            )
            logger.info("Bot Chat Menu Button updated with URL: %s", web_app_url)
    except Exception as e:
        logger.warning("Failed to set chat menu button: %s", e)

def get_webapp_url(user_id=None, username=None) -> str:
    """Returns the HTTPS WebApp URL with embedded user parameters for seamless session recovery."""
    base = config.WEBAPP_URL or ""
    if not base or not base.startswith("http"):
        return "https://telegram.org"
    if user_id:
        param = f"user_id={user_id}"
        if username:
            param += f"&username={username}"
        sep = "&" if "?" in base else "?"
        return f"{base}{sep}{param}"
    return base

async def create_stars_invoice(title: str, description: str, payload: str, stars_amount: int) -> str:
    """Creates a native Telegram Stars (XTR) invoice link."""
    bot = get_bot_instance()
    return await bot.create_invoice_link(
        title=title,
        description=description,
        payload=payload,
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=title, amount=max(1, int(stars_amount)))]
    )

async def notify_customer_order(order: dict, event: str = "created"):
    """Sends an automated Telegram notification to the customer about their order."""
    bot = get_bot_instance()
    user_id = order.get("user_id")
    if not user_id:
        return
        
    order_uuid = order.get("order_uuid")
    product_name = html.escape(str(order.get("product_name", "")))
    target = html.escape(str(order.get("target_recipient", "")))
    price_stars = order.get("price_stars")
    price_usd = order.get("price_usd")
    status = order.get("status")

    if event == "created":
        text = (
            f"🛒 <b>Order Received!</b>\n\n"
            f"🆔 <b>Order ID:</b> <code>#{order_uuid}</code>\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"🎯 <b>Recipient Telegram Account:</b> <code>{target}</code>\n"
            f"💰 <b>Total:</b> {price_stars} ⭐ (${price_usd})\n"
            f"📊 <b>Status:</b> ⏳ Pending Payment/Fulfillment\n\n"
            f"Your order is being processed for delivery to your Telegram ID account!"
        )
    elif event == "paid":
        text = (
            f"🎉 <b>Payment Confirmed!</b>\n\n"
            f"🆔 <b>Order ID:</b> <code>#{order_uuid}</code>\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"🎯 <b>Recipient Telegram Account:</b> <code>{target}</code>\n"
            f"💰 <b>Paid:</b> {price_stars} ⭐\n"
            f"📊 <b>Status:</b> 🚀 Processing Delivery\n\n"
            f"Thank you! Your order is being delivered to <code>{target}</code>."
        )
    elif event == "completed":
        text = (
            f"✅ <b>Order Delivered to Account!</b>\n\n"
            f"🆔 <b>Order ID:</b> <code>#{order_uuid}</code>\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"🎯 <b>Delivered to Telegram Account:</b> <code>{target}</code>\n"
            f"📊 <b>Status:</b> ✅ Delivered\n\n"
            f"Your purchase has been delivered successfully to your account!"
        )
    elif event == "cancelled":
        text = (
            f"❌ <b>Order Cancelled</b>\n\n"
            f"🆔 <b>Order ID:</b> <code>#{order_uuid}</code>\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"If you paid or have questions, please contact customer support."
        )
    else:
        text = f"ℹ️ <b>Order Update:</b> #{order_uuid} status is now <b>{status.upper()}</b>."

    try:
        await bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Failed to send notification to user {user_id}: {e}")

async def notify_admins(order: dict):
    """Sends notification to orders channel and all registered admin IDs."""
    bot = get_bot_instance()
    order_uuid = order.get("order_uuid")
    product_name = html.escape(str(order.get("product_name", "")))
    target = html.escape(str(order.get("target_recipient", "")))
    price_stars = order.get("price_stars")
    price_usd = order.get("price_usd")
    user_name = html.escape(str(order.get("user_name", "")))
    payment_method = str(order.get("payment_method", "")).upper()
    category = str(order.get("category", "")).capitalize()
    
    admin_text = (
        f"🚨 <b>New Store Order!</b> #{order_uuid}\n\n"
        f"📂 <b>Category:</b> {category}\n"
        f"👤 <b>Customer:</b> {user_name} (<code>{order.get('user_id')}</code>)\n"
        f"📦 <b>Product:</b> {product_name}\n"
        f"🎯 <b>Recipient Telegram Account:</b> <code>{target}</code>\n"
        f"💰 <b>Price:</b> {price_stars} ⭐ / ${price_usd}\n"
        f"💳 <b>Payment Method:</b> {payment_method}\n"
        f"📊 <b>Status:</b> {order.get('status')}"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Mark Done", callback_data=f"adm_done_{order_uuid}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"adm_cancel_{order_uuid}")
        ]
    ])

    # 1. Post to Dedicated Orders Channel if configured
    orders_channel = database.get_setting("orders_channel_id") or config.ORDERS_CHANNEL_ID
    if orders_channel:
        try:
            await bot.send_message(
                chat_id=orders_channel,
                text=admin_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            logger.info("Order alert posted to channel %s", orders_channel)
        except Exception as e:
            logger.error(f"Failed to post order to channel {orders_channel}: {e}")

    # 2. Direct message to admin users
    admins = list(config.ADMIN_IDS)
    try:
        with database.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE is_admin = 1")
            for row in cursor.fetchall():
                if row["id"] not in admins:
                    admins.append(row["id"])
    except Exception as e:
        logger.warning("Error fetching admin IDs: %s", e)

    for admin_id in admins:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Failed to notify admin {admin_id}: {e}")

# Command Handlers
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args or []
    
    referrer_id = None
    is_admin = 1 if (args and args[0] == "admin_setup") or (user.id in config.ADMIN_IDS) else 0
    if is_admin and user.id not in config.ADMIN_IDS:
        config.ADMIN_IDS.append(user.id)
        
    # Check if user came via referral link (e.g. /start ref_12345678)
    if args and args[0].startswith("ref_"):
        try:
            ref_candidate = int(args[0].replace("ref_", ""))
            if ref_candidate != user.id:
                referrer_id = ref_candidate
        except ValueError:
            pass

    u_data = database.upsert_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_admin=is_admin,
        referrer_id=referrer_id
    )

    # Notify referrer if this is a newly linked referral
    bot = get_bot_instance()
    if referrer_id and u_data.get("referrer_id") == referrer_id:
        try:
            ref_name = html.escape(user.first_name or "A friend")
            ref_handle = f" (@{user.username})" if user.username else ""
            await bot.send_message(
                chat_id=referrer_id,
                text=(
                    f"👥 <b>New Friend Joined!</b>\n\n"
                    f"{ref_name}{ref_handle} joined via your referral link.\n"
                    f"You will earn a <b>5% commission in Stars ⭐</b> on every purchase they make!"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Failed to notify referrer {referrer_id}: {e}")
    
    web_url = get_webapp_url(user.id, user.username)
    safe_name = html.escape(user.first_name or "Friend")
    user_balance = u_data.get("balance_stars", 0)
    
    welcome_text = (
        f"👋 <b>Welcome to Telegram Market, {safe_name}!</b> 🌟\n\n"
        f"🆔 <b>Your Telegram ID:</b> <code>{user.id}</code>\n"
        f"⭐ <b>Stars Balance:</b> <code>{user_balance} ⭐</code>\n\n"
        f"Available services delivered directly to your Telegram account:\n"
        f"⭐ <b>Buy Telegram Stars:</b> Instant delivery to your Telegram ID account (Min. 50 Stars like Fragment)\n"
        f"💎 <b>Telegram Premium:</b> 3, 6, and 12 months subscriptions with instant Telegram payments\n"
        f"🎁 <b>Official Telegram Gifts:</b> 15 ⭐ to 100 ⭐ collectible gifts for profiles\n"
        f"👥 <b>Referral Rewards:</b> Earn 5% commission in Stars on friend purchases\n\n"
        f"Choose an option below or open the Web App:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛒 Launch Market App", web_app=WebAppInfo(url=web_url))],
        [
            InlineKeyboardButton("⭐ Buy Stars (Min 50)", callback_data="view_stars"),
            InlineKeyboardButton("💎 Telegram Premium", callback_data="view_premium")
        ],
        [
            InlineKeyboardButton("🎁 Profile Gifts (15-100⭐)", callback_data="view_gifts"),
            InlineKeyboardButton("👥 Referral Link", callback_data="my_ref")
        ],
        [
            InlineKeyboardButton("📦 My Orders", callback_data="my_orders"),
            InlineKeyboardButton("💬 Support & Help", callback_data="help_info")
        ]
    ]
    if is_admin:
        keyboard.append([InlineKeyboardButton("👑 Admin Dashboard", callback_data="admin_dashboard")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        if config.WEBAPP_URL and config.WEBAPP_URL.startswith("https://"):
            await update.effective_chat.set_menu_button(
                menu_button=MenuButtonWebApp(text="🛒 Market", web_app=WebAppInfo(url=config.WEBAPP_URL))
            )
    except Exception as e:
        logger.warning(f"Could not set menu button in chat: {e}")
        
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="HTML")

async def stars_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows Stars packages starting from minimum 50 Stars (Fragment style)."""
    user = update.effective_user
    text = (
        f"⭐ <b>Buy Telegram Stars to Account</b>\n\n"
        f"Buy Telegram Stars directly to your Telegram ID account (Fragment style).\n"
        f"⚡ <b>Minimum order:</b> 50 Stars\n\n"
        f"Select a Stars package to purchase:"
    )
    buttons = [
        [
            InlineKeyboardButton("⭐ 50 Stars ($0.99)", callback_data="pay_stars_50"),
            InlineKeyboardButton("⭐ 100 Stars ($1.89)", callback_data="pay_stars_100")
        ],
        [
            InlineKeyboardButton("⭐ 250 Stars ($4.49)", callback_data="pay_stars_250"),
            InlineKeyboardButton("⭐ 500 Stars ($8.49)", callback_data="pay_stars_500")
        ],
        [
            InlineKeyboardButton("⭐ 1,000 Stars ($15.99)", callback_data="pay_stars_1000"),
            InlineKeyboardButton("⭐ 2,500 Stars ($36.99)", callback_data="pay_stars_2500")
        ],
        [
            InlineKeyboardButton("⭐ 5,000 Stars ($69.99)", callback_data="pay_stars_5000")
        ],
        [
            InlineKeyboardButton("🛒 Open Web App (Custom Stars)", web_app=WebAppInfo(url=get_webapp_url(user.id, user.username)))
        ]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")

async def premium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows Telegram Premium subscriptions (3 months, 6 months, 1 year)."""
    user = update.effective_user
    text = (
        f"💎 <b>Telegram Premium Subscriptions</b>\n\n"
        f"Unlock double limits, 4GB uploads, voice-to-text, animated emoji, custom app icons, and exclusive badges!\n\n"
        f"⚡ Delivered directly to your Telegram account via Telegram Payments.\n\n"
        f"Choose your subscription duration:"
    )
    buttons = [
        [InlineKeyboardButton("💎 3 Months Premium (600 ⭐ / $11.99)", callback_data="pay_prem_3m")],
        [InlineKeyboardButton("💎 6 Months Premium (850 ⭐ / $16.99)", callback_data="pay_prem_6m")],
        [InlineKeyboardButton("💎 12 Months (1 Year) Premium (1,450 ⭐ / $28.99)", callback_data="pay_prem_12m")],
        [InlineKeyboardButton("🛒 Open in Market App", web_app=WebAppInfo(url=get_webapp_url(user.id, user.username)))]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")

async def gifts_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows official Telegram Gifts ranging from 15 Stars to 100 Stars."""
    user = update.effective_user
    text = (
        f"🎁 <b>Official Telegram Gifts (15 to 100 Stars)</b>\n\n"
        f"Collectible gifts displayed on your Telegram profile or convertible into Stars!\n\n"
        f"Select a gift to buy to your account:"
    )
    buttons = [
        [
            InlineKeyboardButton("❤️ Heart (15 ⭐)", callback_data="pay_gift_heart"),
            InlineKeyboardButton("🧸 Bear (15 ⭐)", callback_data="pay_gift_bear")
        ],
        [
            InlineKeyboardButton("🎁 Gift (25 ⭐)", callback_data="pay_gift_box"),
            InlineKeyboardButton("🌹 Rose (25 ⭐)", callback_data="pay_gift_rose")
        ],
        [
            InlineKeyboardButton("🎂 Birthday Cake (50 ⭐)", callback_data="pay_gift_cake"),
            InlineKeyboardButton("💐 Bouquet of Flowers (50 ⭐)", callback_data="pay_gift_bouquet")
        ],
        [
            InlineKeyboardButton("🚀 A Rocket (50 ⭐)", callback_data="pay_gift_rocket"),
            InlineKeyboardButton("🍾 Champagne (50 ⭐)", callback_data="pay_gift_champagne")
        ],
        [
            InlineKeyboardButton("🏆 Champions Cup (100 ⭐)", callback_data="pay_gift_cup"),
            InlineKeyboardButton("💍 A Ring (100 ⭐)", callback_data="pay_gift_ring")
        ],
        [
            InlineKeyboardButton("💎 A Diamond (100 ⭐)", callback_data="pay_gift_diamond")
        ],
        [
            InlineKeyboardButton("🛒 Open Web App for Gifts", web_app=WebAppInfo(url=get_webapp_url(user.id, user.username)))
        ]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")

async def market_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    web_url = get_webapp_url(user.id, user.username)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Open Market App", web_app=WebAppInfo(url=web_url))]
    ])
    await update.message.reply_text("Tap below to open the Market Web App:", reply_markup=keyboard)

async def referral_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    user_db = database.get_user(user_id) or {}
    
    bot = get_bot_instance()
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    invited = user_db.get("referral_count", 0)
    earnings = user_db.get("referral_earnings", 0)
    
    text = (
        f"👥 <b>Referral & Earn System</b>\n\n"
        f"Invite friends and earn <b>5% commission in Stars ⭐</b> on all their purchases!\n\n"
        f"🔗 <b>Your Invite Link:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        f"📊 <b>Your Referral Stats:</b>\n"
        f"• Friends Invited: <b>{invited}</b>\n"
        f"• Total Stars Earned: <b>{earnings} ⭐</b>\n"
        f"• Commission Rate: <b>5%</b>\n\n"
        f"Share your link and earn Telegram Stars passively!"
    )
    
    share_url = f"https://t.me/share/url?url={ref_link}&text=Join%20the%20Telegram%20Market%20for%20Stars,%20Premium%20and%20Gifts!"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Share with Friends", url=share_url)],
        [InlineKeyboardButton("🛒 Open Market App", web_app=WebAppInfo(url=get_webapp_url(user.id, user.username)))]
    ])
    
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    user_db = database.get_user(user_id) or {}
    bal = user_db.get("balance_stars", 0)
    
    text = (
        f"💰 <b>Your Stars Balance</b>\n\n"
        f"⭐ Current Balance: <b>{bal} Stars</b>\n\n"
        f"You can use your Stars balance to buy Telegram Premium or Collectible Gifts instantly with 1 tap!"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Buy Stars to Account", callback_data="view_stars")],
        [InlineKeyboardButton("🛒 Open Market", web_app=WebAppInfo(url=get_webapp_url(user.id, user.username)))]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

async def orders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    orders = database.get_user_orders(user_id)
    
    if not orders:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Explore Catalog", web_app=WebAppInfo(url=get_webapp_url(user.id, user.username)))]
        ])
        await update.message.reply_text(
            "You haven't placed any orders yet. Visit the Market to get started!",
            reply_markup=keyboard
        )
        return
        
    lines = ["📋 <b>Your Recent Orders:</b>\n"]
    for o in orders[:8]:
        status_emoji = {"pending": "⏳", "paid": "💳", "processing": "🚀", "completed": "✅", "cancelled": "❌"}.get(o["status"], "ℹ️")
        lines.append(
            f"{status_emoji} <b>#{o['order_uuid']}</b> — {html.escape(o['product_name'])}\n"
            f"   🎯 <code>{html.escape(o['target_recipient'])}</code> | {o['price_stars']} ⭐ (${o['price_usd']})\n"
            f"   Status: <code>{o['status'].capitalize()}</code>\n"
        )
        
    lines.append("\nYou can track live progress inside the Web App under <b>My Orders</b>.")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        f"📖 <b>Telegram Market Guide & Help</b>\n\n"
        f"⭐ <b>Buy Telegram Stars:</b>\n"
        f"Deposited directly to your Telegram ID account. Minimum 50 Stars (Fragment style).\n\n"
        f"💎 <b>Telegram Premium:</b>\n"
        f"3 months, 6 months, or 12 months (1 year) subscriptions via Telegram Payments. Instant activation!\n\n"
        f"🎁 <b>Official Telegram Gifts:</b>\n"
        f"Profile gifts ranging from 15 Stars to 100 Stars (Heart, Bear, Star, Cake, Trophy, Diamond, etc.).\n\n"
        f"👥 <b>Referral Program:</b>\n"
        f"Earn 5% commission in Stars on every order placed by friends you invite!"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")

async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in config.ADMIN_IDS:
        database.upsert_user(user_id=user_id, username=update.effective_user.username, first_name=update.effective_user.first_name, is_admin=1)
        config.ADMIN_IDS.append(user_id)
        
    stats = database.get_stats()
    all_orders = database.get_all_orders(limit=10)
    ch_info = database.get_setting("orders_channel_id") or config.ORDERS_CHANNEL_ID or "Not connected (Use /setchannel @YourChannel)"
    
    text = (
        f"👑 <b>Admin Management Dashboard</b>\n\n"
        f"📢 <b>Orders Channel:</b> <code>{ch_info}</code>\n"
        f"📊 <b>Total Orders:</b> {stats['total_orders']}\n"
        f"💰 <b>Total Revenue:</b> ${stats['total_usd']} ({stats['total_stars']} ⭐)\n"
        f"⏳ <b>Pending Fulfillment:</b> {stats['pending_count']}\n"
        f"👥 <b>Total Customers:</b> {stats['total_users']}\n\n"
        f"📋 <b>Recent Orders Queue:</b>"
    )
    
    buttons = []
    has_pending = False
    for o in all_orders:
        if o["status"] in ("pending", "paid"):
            has_pending = True
            buttons.append([
                InlineKeyboardButton(f"✅ #{o['order_uuid']} ({o['product_name'][:14]})", callback_data=f"adm_done_{o['order_uuid']}"),
                InlineKeyboardButton("❌", callback_data=f"adm_cancel_{o['order_uuid']}")
            ])
            
    if not has_pending:
        text += "\n<i>No pending orders at the moment.</i>"
        
    buttons.append([InlineKeyboardButton("🔄 Refresh Stats", callback_data="admin_dashboard")])
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")

async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user
    
    # 1. Navigation Menus
    if data == "my_orders":
        await orders_cmd(update, context)
    elif data == "my_ref":
        await referral_cmd(update, context)
    elif data == "help_info":
        await help_cmd(update, context)
    elif data == "view_stars":
        await stars_cmd(update, context)
    elif data == "view_premium":
        await premium_cmd(update, context)
    elif data == "view_gifts":
        await gifts_cmd(update, context)
        
    # 2. Telegram Payments: Subscriptions (3m, 6m, 12m)
    elif data.startswith("pay_prem_"):
        prem_map = {
            "pay_prem_3m": ("3 Months Telegram Premium", 600, 11.99, "prem_3m"),
            "pay_prem_6m": ("6 Months Telegram Premium", 850, 16.99, "prem_6m"),
            "pay_prem_12m": ("12 Months (1 Year) Telegram Premium", 1450, 28.99, "prem_12m")
        }
        item = prem_map.get(data)
        if item:
            title, stars, usd, pid = item
            recipient_handle = f"@{user.username}" if user.username else f"ID: {user.id}"
            
            # Create order record
            order = database.create_order(
                user_id=user.id,
                user_name=recipient_handle,
                category="premium",
                product_id=pid,
                product_name=title,
                quantity=1,
                price_usd=usd,
                price_stars=stars,
                target_recipient=recipient_handle,
                extra_data={"chat_order": True},
                payment_method="stars"
            )
            
            # Send Telegram Stars Invoice directly in chat
            try:
                bot = get_bot_instance()
                await bot.send_invoice(
                    chat_id=user.id,
                    title=title,
                    description=f"Telegram Premium for {recipient_handle}. Instant activation.",
                    payload=f"order_{order['order_uuid']}",
                    provider_token="",
                    currency="XTR",
                    prices=[LabeledPrice(label=title, amount=stars)]
                )
            except Exception as e:
                logger.error(f"Error sending premium invoice: {e}")
                await query.message.reply_text(f"Could not open invoice: {e}")

    # 3. Telegram Payments: Stars Packages (Min. 50 Stars)
    elif data.startswith("pay_stars_"):
        stars_count = int(data.replace("pay_stars_", ""))
        usd_map = {50: 0.99, 100: 1.89, 250: 4.49, 500: 8.49, 1000: 15.99, 2500: 36.99, 5000: 69.99}
        usd = usd_map.get(stars_count, round(stars_count * 0.016, 2))
        recipient_handle = f"@{user.username}" if user.username else f"ID: {user.id}"
        
        order = database.create_order(
            user_id=user.id,
            user_name=recipient_handle,
            category="stars",
            product_id=f"stars_{stars_count}",
            product_name=f"{stars_count} Telegram Stars",
            quantity=1,
            price_usd=usd,
            price_stars=stars_count,
            target_recipient=recipient_handle,
            extra_data={"chat_order": True},
            payment_method="stars"
        )
        
        try:
            bot = get_bot_instance()
            await bot.send_invoice(
                chat_id=user.id,
                title=f"{stars_count} Telegram Stars",
                description=f"Direct delivery to Telegram ID account {recipient_handle}.",
                payload=f"order_{order['order_uuid']}",
                provider_token="",
                currency="XTR",
                prices=[LabeledPrice(label=f"{stars_count} Stars", amount=stars_count)]
            )
        except Exception as e:
            logger.error(f"Error sending stars invoice: {e}")
            await query.message.reply_text(f"Could not open invoice: {e}")

    # 4. Telegram Payments: Gifts (15 to 100 Stars)
    elif data.startswith("pay_gift_"):
        gift_id = data.replace("pay_gift_", "")
        found_gift = None
        for g in catalog.CATALOG["gifts"]["packages"]:
            if g["id"] == f"gift_{gift_id}":
                found_gift = g
                break
                
        if found_gift:
            recipient_handle = f"@{user.username}" if user.username else f"ID: {user.id}"
            order = database.create_order(
                user_id=user.id,
                user_name=recipient_handle,
                category="gifts",
                product_id=found_gift["id"],
                product_name=f"{found_gift['emoji']} {found_gift['name']} Gift",
                quantity=1,
                price_usd=found_gift["price_usd"],
                price_stars=found_gift["price_stars"],
                target_recipient=recipient_handle,
                extra_data={"gift_emoji": found_gift["emoji"]},
                payment_method="stars"
            )
            try:
                bot = get_bot_instance()
                await bot.send_invoice(
                    chat_id=user.id,
                    title=f"{found_gift['emoji']} {found_gift['name']} Gift",
                    description=f"Telegram profile gift for {recipient_handle}.",
                    payload=f"order_{order['order_uuid']}",
                    provider_token="",
                    currency="XTR",
                    prices=[LabeledPrice(label=found_gift["name"], amount=found_gift["price_stars"])]
                )
            except Exception as e:
                logger.error(f"Error sending gift invoice: {e}")
                await query.message.reply_text(f"Could not open invoice: {e}")

    # 5. Admin Dashboard Actions
    elif data == "admin_dashboard":
        stats = database.get_stats()
        all_orders = database.get_all_orders(limit=10)
        text = (
            f"👑 <b>Admin Management Dashboard</b>\n\n"
            f"📊 <b>Total Orders:</b> {stats['total_orders']}\n"
            f"💰 <b>Revenue:</b> ${stats['total_usd']} ({stats['total_stars']} ⭐)\n"
            f"⏳ <b>Pending:</b> {stats['pending_count']}\n"
            f"👥 <b>Users:</b> {stats['total_users']}\n\n"
            f"📋 <b>Orders Queue:</b>"
        )
        buttons = []
        for o in all_orders:
            if o["status"] in ("pending", "paid"):
                buttons.append([
                    InlineKeyboardButton(f"✅ #{o['order_uuid']} ({o['product_name'][:12]})", callback_data=f"adm_done_{o['order_uuid']}"),
                    InlineKeyboardButton("❌", callback_data=f"adm_cancel_{o['order_uuid']}")
                ])
        buttons.append([InlineKeyboardButton("🔄 Refresh", callback_data="admin_dashboard")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons), parse_mode="HTML")
        
    elif data.startswith("adm_done_"):
        order_uuid = data.replace("adm_done_", "")
        order = database.update_order_status(order_uuid, "completed")
        if order:
            try:
                database.reward_referrer_commission(
                    buyer_id=order["user_id"],
                    order_stars=order.get("price_stars", 0)
                )
            except Exception as e:
                logger.warning("Could not reward referral commission: %s", e)
            await notify_customer_order(order, event="completed")
            await query.edit_message_text(f"✅ Order #{order_uuid} marked as COMPLETED and customer notified!")
        else:
            await query.edit_message_text(f"Order #{order_uuid} not found.")
            
    elif data.startswith("adm_cancel_"):
        order_uuid = data.replace("adm_cancel_", "")
        order = database.update_order_status(order_uuid, "cancelled")
        if order:
            await notify_customer_order(order, event="cancelled")
            await query.edit_message_text(f"❌ Order #{order_uuid} cancelled.")

# Native Stars Invoice Handlers
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answers pre-checkout query to approve native Telegram Stars payments."""
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered automatically when a user completes payment via Telegram Stars."""
    msg = update.message
    payment = msg.successful_payment
    payload = payment.invoice_payload
    user_id = msg.from_user.id
    
    # 1. Check if Balance Top-Up
    if payload.startswith("topup_"):
        parts = payload.split("_")
        stars_count = int(parts[2]) if len(parts) >= 3 else payment.total_amount
        
        updated_user = database.add_balance(
            user_id=user_id,
            amount_stars=stars_count,
            tx_type="topup",
            description=f"Telegram Stars Top-Up (+{stars_count} ⭐)"
        )
        new_balance = updated_user.get("balance_stars", stars_count) if updated_user else stars_count
        
        await msg.reply_text(
            f"🎉 <b>Balance Top-Up Successful!</b>\n\n"
            f"⭐ Added: <b>+{stars_count} Stars</b>\n"
            f"💰 Current Balance: <b>{new_balance} Stars</b>\n\n"
            f"You can now purchase Telegram Premium and Collectible Gifts instantly!",
            parse_mode="HTML"
        )
        logger.info(f"Top-up completed for user {user_id}: +{stars_count} Stars")
        return

    # 2. Product Orders (Stars to account, Telegram Premium, or Gifts)
    if payload.startswith("order_"):
        order_uuid = payload.replace("order_", "")
        order = database.update_order_status(
            order_uuid,
            status="paid",
            tx_hash=payment.telegram_payment_charge_id
        )
        
        if order:
            await notify_customer_order(order, event="paid")
            await notify_admins(order)
            
            # Reward referrer commission (5%)
            reward = database.reward_referrer_commission(order["user_id"], order["price_stars"])
            if reward:
                try:
                    bot = get_bot_instance()
                    await bot.send_message(
                        chat_id=reward["referrer_id"],
                        text=(
                            f"🎁 <b>Referral Commission Received!</b>\n\n"
                            f"Your invited friend completed a purchase.\n"
                            f"⭐ <b>+{reward['commission_stars']} Stars</b> credited to your balance!"
                        ),
                        parse_mode="HTML"
                    )
                except Exception as e:
                    logger.warning(f"Could not notify referrer of reward: {e}")
                    
            logger.info(f"Payment received for order {order_uuid}: {payment.total_amount} {payment.currency}")

async def setchannel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sets the dedicated channel for order notifications."""
    args = context.args or []
    current_ch = database.get_setting("orders_channel_id") or config.ORDERS_CHANNEL_ID
    
    if not args:
        status_txt = f"<code>{current_ch}</code>" if current_ch else "<i>Not connected yet</i>"
        await update.message.reply_text(
            f"📢 <b>Orders Channel Settings</b>\n\n"
            f"Current Channel: {status_txt}\n\n"
            f"<b>How to connect your channel:</b>\n"
            f"1. Add the bot to your channel as an <b>Admin</b> with 'Post Messages' permission.\n"
            f"2. Send: <code>/setchannel @YourChannelName</code> or <code>/setchannel -100xxxxxxxxxx</code>\n"
            f"3. Or forward any post from your channel to this bot chat!",
            parse_mode="HTML"
        )
        return

    channel_input = args[0].strip()
    bot = get_bot_instance()
    try:
        test_msg = await bot.send_message(
            chat_id=channel_input,
            text=(
                f"✅ <b>Telegram Market Bot Connected!</b>\n\n"
                f"All customer orders, Stars deliveries, and Telegram payments will appear here."
            ),
            parse_mode="HTML"
        )
        ch_id = str(test_msg.chat.id)
        database.set_setting("orders_channel_id", ch_id)
        config.ORDERS_CHANNEL_ID = ch_id
        await update.message.reply_text(
            f"🎉 <b>Channel Connected Successfully!</b>\n\n"
            f"Channel: <b>{html.escape(test_msg.chat.title or channel_input)}</b>\n"
            f"Channel ID: <code>{ch_id}</code>\n\n"
            f"All new orders will now appear in this channel!",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ <b>Could not connect to channel:</b> {html.escape(str(e))}\n\n"
            f"Please ensure the bot is added as an Administrator with 'Post Messages' permission in that channel.",
            parse_mode="HTML"
        )

async def my_chat_member_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Automatically detects when the bot is added as admin to a channel."""
    chat = update.effective_chat
    if not update.my_chat_member:
        return
    new_member = update.my_chat_member.new_chat_member
    if chat.type in ["channel", "supergroup"]:
        if new_member.status in ["administrator"]:
            ch_id = str(chat.id)
            database.set_setting("orders_channel_id", ch_id)
            config.ORDERS_CHANNEL_ID = ch_id
            logger.info("Bot added as admin to channel %s (%s). Set as orders channel!", chat.title, ch_id)
            try:
                bot = get_bot_instance()
                await bot.send_message(
                    chat_id=chat.id,
                    text="🚀 <b>Telegram Market Bot Connected!</b>\nNew orders and alerts will be posted here.",
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.warning("Could not send confirmation to channel %s: %s", chat.id, e)

async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto-detects channel ID whenever any message is posted in the channel where bot is admin."""
    chat = update.effective_chat
    if chat and chat.type == "channel":
        ch_id = str(chat.id)
        current = database.get_setting("orders_channel_id")
        if not current:
            database.set_setting("orders_channel_id", ch_id)
            config.ORDERS_CHANNEL_ID = ch_id
            logger.info("Auto-registered orders channel from post: %s (%s)", chat.title, ch_id)

async def handle_forwarded_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detects when an admin forwards a message from a channel."""
    msg = update.effective_message
    if msg and msg.forward_from_chat and msg.forward_from_chat.type == "channel":
        ch = msg.forward_from_chat
        ch_id = str(ch.id)
        database.set_setting("orders_channel_id", ch_id)
        config.ORDERS_CHANNEL_ID = ch_id
        await msg.reply_text(
            f"📢 <b>Channel Detected & Connected!</b>\n\n"
            f"Channel: <b>{html.escape(ch.title or 'Channel')}</b>\n"
            f"ID: <code>{ch_id}</code>\n\n"
            f"Set as the orders channel! All new orders will appear here.",
            parse_mode="HTML"
        )

def setup_application():
    global bot_app
    bot_app = Application.builder().token(config.BOT_TOKEN).build()
    
    # Register handlers
    bot_app.add_handler(CommandHandler("start", start_cmd))
    bot_app.add_handler(CommandHandler("market", market_cmd))
    bot_app.add_handler(CommandHandler("stars", stars_cmd))
    bot_app.add_handler(CommandHandler("premium", premium_cmd))
    bot_app.add_handler(CommandHandler("subscriptions", premium_cmd))
    bot_app.add_handler(CommandHandler("gifts", gifts_cmd))
    bot_app.add_handler(CommandHandler("balance", balance_cmd))
    bot_app.add_handler(CommandHandler("ref", referral_cmd))
    bot_app.add_handler(CommandHandler("referral", referral_cmd))
    bot_app.add_handler(CommandHandler("orders", orders_cmd))
    bot_app.add_handler(CommandHandler("help", help_cmd))
    bot_app.add_handler(CommandHandler("admin", admin_cmd))
    bot_app.add_handler(CommandHandler("setchannel", setchannel_cmd))
    
    bot_app.add_handler(ChatMemberHandler(my_chat_member_handler, ChatMemberHandler.MY_CHAT_MEMBER))
    bot_app.add_handler(MessageHandler(filters.ChatType.CHANNEL, channel_post_handler))
    bot_app.add_handler(MessageHandler(filters.FORWARDED & filters.ChatType.PRIVATE, handle_forwarded_post))
    
    bot_app.add_handler(CallbackQueryHandler(callback_router))
    bot_app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    bot_app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    
    return bot_app
