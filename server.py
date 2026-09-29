import os
import uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any

import config
import database
import catalog
import bot_service

app = FastAPI(title="Telegram Market Web App API")

# Enable CORS for Telegram WebApp environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Content-Security-Policy"] = "frame-ancestors * https://*.telegram.org https://web.telegram.org;"
    if "x-frame-options" in response.headers:
        del response.headers["x-frame-options"]
    return response

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Mount static folder
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Frontend index.html not found")
    return FileResponse(str(index_file))

@app.get("/health")
@app.get("/ping")
async def health_check():
    return {"status": "ok", "service": "telegram_market_bot", "alive": True}

# Models
class CreateOrderRequest(BaseModel):
    user_id: int
    user_name: Optional[str] = "Customer"
    category: str  # reactions, premium, gifts
    product_id: str
    product_name: str
    quantity: int = 1
    price_usd: float
    price_stars: int
    target_recipient: str
    extra_data: Optional[Dict[str, Any]] = None
    payment_method: str = "stars"  # balance, stars, ton, usdt, card

class TopUpRequest(BaseModel):
    user_id: int
    stars_count: int

class TonTopUpRequest(BaseModel):
    user_id: int
    user_name: Optional[str] = "Customer"
    stars_count: int
    ton_amount: float
    tx_hash: Optional[str] = ""

class UpdateStatusRequest(BaseModel):
    status: str
    tx_hash: Optional[str] = None

@app.get("/api/config")
async def get_app_config():
    return {
        "bot_username": "vst_starsmarket_bot",
        "crypto": config.CRYPTO_CONFIG,
        "card": config.CARD_CONFIG,
        "admin_ids": config.ADMIN_IDS
    }

@app.get("/api/catalog")
async def get_catalog():
    return {
        "ok": True,
        "catalog": catalog.CATALOG
    }

@app.get("/api/user/{user_id}")
async def get_user_profile(user_id: int):
    user = database.get_user(user_id)
    if not user:
        user = database.upsert_user(user_id=user_id, username=None, first_name="User")
        
    return {
        "ok": True,
        "user": user,
        "referral_link": f"https://t.me/vst_starsmarket_bot?start=ref_{user_id}"
    }

@app.post("/api/balance/topup")
async def create_topup_invoice(req: TopUpRequest):
    if req.stars_count < 10:
        raise HTTPException(status_code=400, detail="Minimum top-up is 10 Stars")

    topup_uuid = str(uuid.uuid4())[:8]
    payload = f"topup_{req.user_id}_{req.stars_count}_{topup_uuid}"

    try:
        invoice_link = await bot_service.create_stars_invoice(
            title=f"Top Up {req.stars_count} Stars",
            description=f"Deposit {req.stars_count} Telegram Stars directly to your in-app wallet balance.",
            payload=payload,
            stars_amount=req.stars_count
        )
        return {
            "ok": True,
            "invoice_link": invoice_link,
            "stars_count": req.stars_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/balance/topup/ton")
async def create_ton_topup_request(req: TonTopUpRequest):
    if req.stars_count < 10:
        raise HTTPException(status_code=400, detail="Minimum top-up is 10 Stars")
    
    database.upsert_user(user_id=req.user_id, username=req.user_name)
    
    order = database.create_order(
        user_id=req.user_id,
        user_name=req.user_name,
        category="topup",
        product_id=f"topup_ton_{req.stars_count}",
        product_name=f"Top-Up +{req.stars_count} Stars (TON)",
        quantity=1,
        price_usd=round(req.stars_count * 0.019, 2),
        price_stars=req.stars_count,
        target_recipient=req.user_name or f"ID: {req.user_id}",
        extra_data={
            "ton_amount": req.ton_amount,
            "tx_hash": req.tx_hash,
            "wallet": config.CRYPTO_CONFIG["TON"]["address"]
        },
        payment_method="ton"
    )
    
    if req.tx_hash:
        database.update_order_status(order["order_uuid"], "pending", tx_hash=req.tx_hash)
        
    try:
        await bot_service.notify_admins(order)
        await bot_service.notify_customer_order(order, event="created")
    except Exception as e:
        print(f"Top-up notification error: {e}")
        
    return {
        "ok": True,
        "order": order,
        "message": f"Top-up request for +{req.stars_count} Stars submitted! Once confirmed, Stars will be added to your balance."
    }

@app.post("/api/orders/create")
async def api_create_order(req: CreateOrderRequest):
    try:
        invoice_link = None
        order_status = "pending"

        # 1. Minimum 50 Stars check for Stars purchases (Fragment standard)
        if req.category == "stars" and req.price_stars < 50:
            raise HTTPException(status_code=400, detail="Minimum purchase is 50 Telegram Stars (Fragment standard).")

        # 2. Paying for products with existing Stars balance
        if req.payment_method == "balance":
            success = database.deduct_balance(
                user_id=req.user_id,
                amount_stars=req.price_stars,
                tx_type="purchase",
                description=f"Purchased {req.product_name}"
            )
            if not success:
                raise HTTPException(status_code=400, detail="Insufficient Stars balance! Please top up your balance.")
            order_status = "paid"

        # Ensure user exists in database
        database.upsert_user(user_id=req.user_id, username=req.user_name)

        # Save order to DB
        order = database.create_order(
            user_id=req.user_id,
            user_name=req.user_name,
            category=req.category,
            product_id=req.product_id,
            product_name=req.product_name,
            quantity=req.quantity,
            price_usd=req.price_usd,
            price_stars=req.price_stars,
            target_recipient=req.target_recipient,
            extra_data=req.extra_data,
            payment_method=req.payment_method
        )

        if req.payment_method == "balance":
            database.update_order_status(order["order_uuid"], "paid", tx_hash="IN_APP_BALANCE")
            order["status"] = "paid"
            
            # Reward referrer commission (5%)
            reward = database.reward_referrer_commission(req.user_id, req.price_stars)
            if reward:
                try:
                    bot = bot_service.get_bot_instance()
                    await bot.send_message(
                        chat_id=reward["referrer_id"],
                        text=(
                            f"🎁 <b>Referral Reward Received!</b>\n\n"
                            f"A friend you invited made a purchase.\n"
                            f"⭐ <b>+{reward['commission_stars']} Stars</b> credited to your balance!"
                        ),
                        parse_mode="HTML"
                    )
                except Exception:
                    pass

        # If paying via direct Telegram Stars invoice
        elif req.payment_method == "stars":
            try:
                invoice_link = await bot_service.create_stars_invoice(
                    title=f"{req.product_name[:30]}",
                    description=f"Order #{order['order_uuid']} - Delivery to {req.target_recipient}",
                    payload=f"order_{order['order_uuid']}",
                    stars_amount=max(1, int(req.price_stars))
                )
            except Exception as e:
                print(f"Error generating Stars invoice link: {e}")

        # Send instant notification to customer via bot
        try:
            await bot_service.notify_customer_order(order, event="paid" if order_status == "paid" else "created")
        except Exception as e:
            print(f"Notification error: {e}")
            
        # Alert admins
        try:
            await bot_service.notify_admins(order)
        except Exception as e:
            print(f"Admin notification error: {e}")

        # Refresh user balance
        u = database.get_user(req.user_id)
        current_balance = u.get("balance_stars", 0) if u else 0

        return {
            "ok": True,
            "order": order,
            "invoice_link": invoice_link,
            "new_balance": current_balance
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/referrals/{user_id}")
async def get_referrals(user_id: int):
    user = database.get_user(user_id) or {}
    refs = database.get_user_referrals(user_id)
    return {
        "ok": True,
        "referral_count": user.get("referral_count", 0),
        "referral_earnings": user.get("referral_earnings", 0),
        "referrals": refs,
        "referral_link": f"https://t.me/vst_starsmarket_bot?start=ref_{user_id}"
    }

@app.get("/api/orders/user/{user_id}")
async def get_user_orders(user_id: int):
    orders = database.get_user_orders(user_id)
    return {
        "ok": True,
        "orders": orders
    }

@app.get("/api/orders/{order_id}")
async def get_order_details(order_id: str):
    order = database.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "ok": True,
        "order": order
    }

@app.post("/api/orders/{order_id}/mark-paid")
async def mark_order_paid(order_id: str, req: UpdateStatusRequest):
    order = database.update_order_status(order_id, "paid", tx_hash=req.tx_hash)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    await bot_service.notify_customer_order(order, event="paid")
    await bot_service.notify_admins(order)
    return {"ok": True, "order": order}

@app.get("/api/admin/orders")
async def get_admin_orders(limit: int = 50):
    orders = database.get_all_orders(limit=limit)
    stats = database.get_stats()
    return {
        "ok": True,
        "stats": stats,
        "orders": orders
    }

@app.post("/api/admin/orders/{order_id}/status")
async def update_admin_order_status(order_id: str, req: UpdateStatusRequest):
    order = database.update_order_status(order_id, req.status, tx_hash=req.tx_hash)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    await bot_service.notify_customer_order(order, event=req.status)
    return {"ok": True, "order": order}
