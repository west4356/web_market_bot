import asyncio
import logging
import html
from telegram import (
    Update,
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
    ContextTypes,
    filters
)
import config
import database

logger = logging.getLogger(__name__)

# Global bot application instance
bot_app = None

async def set_menu_button(web_app_url: str):
    """Configures the default Telegram bottom-left Menu Button to open the Web App."""
    if not bot_app:
        return
    try:
        if web_app_url and web_app_url.startswith("https://"):
            await bot_app.bot.set_chat_menu_button(
                menu_button=MenuButtonWebApp(text="🛒 Market", web_app=WebAppInfo(url=web_app_url))
            )
            logger.info("Bot Chat Menu Button updated with URL: %s", web_app_url)
    except Exception as e:
        logger.warning("Failed to set chat menu button: %s", e)

async def create_stars_invoice(title: str, description: str, payload: str, stars_amount: int) -> str:
    """Creates a native Telegram Stars (XTR) invoice link."""
    if not bot_app:
        raise RuntimeError("Bot application not initialized")
    
    return await bot_app.bot.create_invoice_link(
        title=title,
        description=description,
        payload=payload,
        provider_token="",
        currency="XTR",
        prices=[LabeledPrice(label=title, amount=stars_amount)]
    )

async def notify_customer_order(order: dict, event: str = "created"):
    """Sends an automated Telegram notification to the customer about their order."""
    if not bot_app:
        return
    
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
            f"🎯 <b>Target:</b> <code>{target}</code>\n"
            f"💰 <b>Total:</b> {price_stars} ⭐ (${price_usd})\n"
            f"📊 <b>Status:</b> ⏳ Pending\n\n"
            f"We are processing your order. You will receive an update once it is delivered!"
        )
    elif event == "paid":
        text = (
            f"🎉 <b>Payment Confirmed!</b>\n\n"
            f"🆔 <b>Order ID:</b> <code>#{order_uuid}</code>\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"🎯 <b>Target:</b> <code>{target}</code>\n"
            f"💰 <b>Paid:</b> {price_stars} ⭐\n"
            f"📊 <b>Status:</b> 🚀 Processing\n\n"
            f"Thank you! Your order has been placed in the fulfillment queue."
        )
    elif event == "completed":
        text = (
            f"✅ <b>Order Completed & Delivered!</b>\n\n"
            f"🆔 <b>Order ID:</b> <code>#{order_uuid}</code>\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"🎯 <b>Target:</b> <code>{target}</code>\n"
            f"📊 <b>Status:</b> ✅ Delivered\n\n"
            f"Thank you for choosing our Market! Enjoy your Stars/Premium/Gifts."
        )
    elif event == "cancelled":
        text = (
            f"❌ <b>Order Cancelled</b>\n\n"
            f"🆔 <b>Order ID:</b> <code>#{order_uuid}</code>\n"
            f"📦 <b>Product:</b> {product_name}\n"
            f"If you paid or have questions, please reach out to customer support."
        )
    else:
        text = f"ℹ️ <b>Order Update:</b> #{order_uuid} is now <b>{status.upper()}</b>."

    try:
        await bot_app.bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Failed to send notification to user {user_id}: {e}")

async def notify_admins(order: dict):
    """Sends notification to all registered admin IDs."""
    if not bot_app:
        return
    
    admins = list(config.ADMIN_IDS)
    with database.get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE is_admin = 1")
        for row in cursor.fetchall():
            if row["id"] not in admins:
                admins.append(row["id"])
                
    # 1. Post to Dedicated Orders Channel if configured
    if config.ORDERS_CHANNEL_ID:
        try:
            await bot_app.bot.send_message(
                chat_id=config.ORDERS_CHANNEL_ID,
                text=admin_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            logger.info("Order alert posted to channel %s", config.ORDERS_CHANNEL_ID)
        except Exception as e:
            logger.error(f"Failed to post order to channel {config.ORDERS_CHANNEL_ID}: {e}")

    if not admins and not config.ORDERS_CHANNEL_ID:
        return
        
    order_uuid = order.get("order_uuid")
    product_name = html.escape(str(order.get("product_name", "")))
    target = html.escape(str(order.get("target_recipient", "")))
    price_stars = order.get("price_stars")
    price_usd = order.get("price_usd")
    user_name = html.escape(str(order.get("user_name", "")))
    payment_method = order.get("payment_method")
    
    admin_text = (
        f"🚨 <b>New Market Order!</b> #{order_uuid}\n\n"
        f"👤 <b>Customer:</b> {user_name} (<code>{order.get('user_id')}</code>)\n"
        f"📦 <b>Product:</b> {product_name}\n"
        f"🎯 <b>Recipient/Link:</b> <code>{target}</code>\n"
        f"💰 <b>Price:</b> {price_stars} ⭐ / ${price_usd}\n"
        f"💳 <b>Payment:</b> {payment_method.upper()}\n"
        f"📊 <b>Status:</b> {order.get('status')}"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Mark Done", callback_data=f"adm_done_{order_uuid}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"adm_cancel_{order_uuid}")
        ]
    ])
    
    for admin_id in admins:
        try:
            await bot_app.bot.send_message(
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
    if referrer_id and u_data.get("referrer_id") == referrer_id:
        try:
            ref_name = html.escape(user.first_name or "A friend")
            ref_handle = f" (@{user.username})" if user.username else ""
            await bot_app.bot.send_message(
                chat_id=referrer_id,
                text=(
                    f"👥 <b>New Friend Joined!</b>\n\n"
                    f"{ref_name}{ref_handle} joined the Market via your referral link.\n"
                    f"You will earn a <b>5% commission in Stars ⭐</b> on every purchase they make!"
                ),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Failed to notify referrer {referrer_id}: {e}")
    
    web_url = config.WEBAPP_URL or "https://telegram.org"
    safe_name = html.escape(user.first_name or "Friend")
    user_balance = u_data.get("balance_stars", 0)
    
    welcome_text = (
        f"👋 <b>Welcome to Telegram Market, {safe_name}!</b> 🌟\n\n"
        f"💰 <b>Your Stars Balance:</b> <code>{user_balance} ⭐</code>\n\n"
        f"Here you can purchase premium Telegram services seamlessly:\n"
        f"⭐ <b>Paid Reactions:</b> Boost posts & rankings\n"
        f"💎 <b>Telegram Premium:</b> 3, 6, 12 months gifting\n"
        f"🎁 <b>Official Telegram Gifts:</b> 15 ⭐ to 2,500 ⭐ gifts\n"
        f"👥 <b>Referral Rewards:</b> Earn 5% commission in Stars\n\n"
        f"Tap the button below to launch the store!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛒 Launch Market App", web_app=WebAppInfo(url=web_url))],
        [
            InlineKeyboardButton("⭐ Top Up Balance", callback_data="topup_menu"),
            InlineKeyboardButton("👥 Referral Link", callback_data="my_ref")
        ],
        [
            InlineKeyboardButton("📦 My Orders", callback_data="my_orders"),
            InlineKeyboardButton("💬 Support & FAQ", callback_data="help_info")
        ]
    ]
    if is_admin:
        keyboard.append([InlineKeyboardButton("⚙️ Admin Dashboard", callback_data="admin_dashboard")])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        if config.WEBAPP_URL and config.WEBAPP_URL.startswith("https://"):
            await update.effective_chat.set_menu_button(
                menu_button=MenuButtonWebApp(text="🛒 Market", web_app=WebAppInfo(url=config.WEBAPP_URL))
            )
    except Exception as e:
        logger.warning(f"Could not set menu button in chat: {e}")
        
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="HTML")

async def market_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_url = config.WEBAPP_URL or "https://telegram.org"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Open Market", web_app=WebAppInfo(url=web_url))]
    ])
    try:
        if config.WEBAPP_URL and config.WEBAPP_URL.startswith("https://"):
            await update.effective_chat.set_menu_button(
                menu_button=MenuButtonWebApp(text="🛒 Market", web_app=WebAppInfo(url=config.WEBAPP_URL))
            )
    except Exception:
        pass
    await update.message.reply_text("Tap below to open the Market Web App:", reply_markup=keyboard)

async def referral_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = database.get_user(user_id) or {}
    
    bot_info = await bot_app.bot.get_me()
    bot_username = bot_info.username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    invited = user.get("referral_count", 0)
    earnings = user.get("referral_earnings", 0)
    
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
        [InlineKeyboardButton("🛒 Open Market App", web_app=WebAppInfo(url=config.WEBAPP_URL or "https://telegram.org"))]
    ])
    
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

async def balance_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = database.get_user(user_id) or {}
    bal = user.get("balance_stars", 0)
    
    text = (
        f"💰 <b>Your Stars Balance</b>\n\n"
        f"⭐ Current Balance: <b>{bal} Stars</b>\n\n"
        f"You can use your Stars balance to buy Paid Reactions, Telegram Premium, or 3D Collectible Gifts instantly with 1 tap!"
    )
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Top Up in Market", web_app=WebAppInfo(url=config.WEBAPP_URL or "https://telegram.org"))]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

async def orders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    orders = database.get_user_orders(user_id)
    
    if not orders:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Explore Catalog", web_app=WebAppInfo(url=config.WEBAPP_URL or "https://telegram.org"))]
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
        f"⭐ <b>Paid Reactions (Stars):</b>\n"
        f"Boost public channel posts. Post link format: <code>t.me/channel/123</code>. Channels receive 85% of stars value.\n\n"
        f"💎 <b>Telegram Premium:</b>\n"
        f"3, 6, 12 months delivered as official gifts to recipient <code>@username</code>. No bank card required!\n\n"
        f"🎁 <b>3D Collectible Gifts:</b>\n"
        f"Modern collectible gifts for profiles. Can be showcased or converted into Stars.\n\n"
        f"💰 <b>Stars Wallet & Balance:</b>\n"
        f"Top up Stars anytime to pay instantly for any product from your in-app balance.\n\n"
        f"👥 <b>Referral Program:</b>\n"
        f"Earn 10% commission on every order placed by friends you invite!"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")

async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in config.ADMIN_IDS:
        database.upsert_user(user_id=user_id, username=update.effective_user.username, first_name=update.effective_user.first_name, is_admin=1)
        config.ADMIN_IDS.append(user_id)
        
    stats = database.get_stats()
    all_orders = database.get_all_orders(limit=10)
    
    text = (
        f"👑 <b>Admin Management Dashboard</b>\n\n"
        f"📊 <b>Total Orders:</b> {stats['total_orders']}\n"
        f"💰 <b>Total Revenue:</b> ${stats['total_usd']} ({stats['total_stars']} ⭐)\n"
        f"⏳ <b>Pending Fulfillment:</b> {stats['pending_count']}\n"
        f"👥 <b>Total Customers:</b> {stats['total_users']}\n\n"
        f"📋 <b>Recent Pending Orders:</b>"
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
    
    if data == "my_orders":
        await orders_cmd(update, context)
    elif data == "my_ref":
        await referral_cmd(update, context)
    elif data == "topup_menu":
        web_url = config.WEBAPP_URL or "https://telegram.org"
        await query.message.reply_text(
            "⭐ <b>Top Up Stars Balance:</b>\nOpen the Web App to select your top-up package:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⭐ Top Up Now", web_app=WebAppInfo(url=web_url))]]),
            parse_mode="HTML"
        )
    elif data == "help_info":
        await help_cmd(update, context)
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
            # Reward referrer 5% commission in Stars
            try:
                database.reward_referrer_commission(
                    buyer_id=order["user_id"],
                    order_stars=order.get("price_stars", 0)
                )
            except Exception as e:
                logger.warning("Could not reward referral commission: %s", e)
            await notify_customer_order(order, event="completed")
            await query.edit_message_text(f"✅ Order #{order_uuid} marked as COMPLETED, customer notified & referral rewarded!")
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
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered automatically when a user completes payment via Telegram Stars."""
    msg = update.message
    payment = msg.successful_payment
    payload = payment.invoice_payload
    user_id = msg.from_user.id
    
    # Check if this is a Balance Top-Up
    if payload.startswith("topup_"):
        # Format: topup_{user_id}_{stars_count}_{uuid}
        parts = payload.split("_")
        stars_count = int(parts[2]) if len(parts) >= 3 else payment.total_amount
        
        # Credit user balance in database
        updated_user = database.add_balance(
            user_id=user_id,
            amount_stars=stars_count,
            tx_type="topup",
            description=f"Telegram Stars Top-Up (+{stars_count} ⭐)"
        )
        
        new_balance = updated_user.get("balance_stars", stars_count) if updated_user else stars_count
        
        # Confirmation message
        await msg.reply_text(
            f"🎉 <b>Balance Top-Up Successful!</b>\n\n"
            f"⭐ Added: <b>+{stars_count} Stars</b>\n"
            f"💰 Current Balance: <b>{new_balance} Stars</b>\n\n"
            f"You can now purchase Paid Reactions, Premium, and Collectible Gifts instantly from your balance!",
            parse_mode="HTML"
        )
        logger.info(f"Top-up completed for user {user_id}: +{stars_count} Stars")
        return

    # Regular Product Order
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
            
            # Check for referral reward
            reward = database.reward_referrer_commission(order["user_id"], order["price_stars"])
            if reward:
                try:
                    await bot_app.bot.send_message(
                        chat_id=reward["referrer_id"],
                        text=(
                            f"🎁 <b>Referral Commission Received!</b>\n\n"
                            f"Your invited friend completed a purchase.\n"
                            f"⭐ <b>+{reward['commission_stars']} Stars</b> added to your balance!\n"
                            f"Keep sharing to earn more!"
                        ),
                        parse_mode="HTML"
                    )
                except Exception as e:
                    logger.warning(f"Could not notify referrer of reward: {e}")
                    
            logger.info(f"Payment received for order {order_uuid}: {payment.total_amount} {payment.currency}")

async def demo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Instantly adds 5000 demo stars to test orders."""
    user_id = update.effective_user.id
    updated_user = database.add_balance(
        user_id=user_id,
        amount_stars=5000,
        tx_type="demo_grant",
        description="Demo test balance (+5000 ⭐)"
    )
    bal = updated_user.get("balance_stars", 5000)
    web_url = config.WEBAPP_URL or "https://telegram.org"
    
    text = (
        f"🎉 <b>5,000 Demo Stars Deposited!</b>\n\n"
        f"⭐ Your Balance: <b>{bal} Stars</b>\n\n"
        f"You can now test purchasing Official Telegram Gifts, Paid Reactions, or Premium directly using your Stars balance with 1 tap!"
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Launch Market App", web_app=WebAppInfo(url=web_url))]
    ])
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="HTML")

def setup_application():
    global bot_app
    bot_app = Application.builder().token(config.BOT_TOKEN).build()
    
    # Register handlers
    bot_app.add_handler(CommandHandler("start", start_cmd))
    bot_app.add_handler(CommandHandler("market", market_cmd))
    bot_app.add_handler(CommandHandler("demo", demo_cmd))
    bot_app.add_handler(CommandHandler("balance", balance_cmd))
    bot_app.add_handler(CommandHandler("ref", referral_cmd))
    bot_app.add_handler(CommandHandler("referral", referral_cmd))
    bot_app.add_handler(CommandHandler("orders", orders_cmd))
    bot_app.add_handler(CommandHandler("help", help_cmd))
    bot_app.add_handler(CommandHandler("admin", admin_cmd))
    
    bot_app.add_handler(CallbackQueryHandler(callback_router))
    bot_app.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    bot_app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    
    return bot_app
