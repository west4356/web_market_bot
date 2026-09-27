import sqlite3
import json
import uuid
from datetime import datetime
from config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                balance_stars INTEGER DEFAULT 0,
                referrer_id INTEGER DEFAULT NULL,
                referral_earnings INTEGER DEFAULT 0,
                referral_count INTEGER DEFAULT 0,
                is_admin INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check and migrate columns if database already existed
        cursor.execute("PRAGMA table_info(users)")
        columns = [row["name"] for row in cursor.fetchall()]
        if "balance_stars" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN balance_stars INTEGER DEFAULT 0")
        if "referrer_id" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN referrer_id INTEGER DEFAULT NULL")
        if "referral_earnings" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN referral_earnings INTEGER DEFAULT 0")
        if "referral_count" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN referral_count INTEGER DEFAULT 0")

        # Referrals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER UNIQUE,
                bonus_stars INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Balance Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS balance_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount_stars INTEGER,
                type TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_uuid TEXT UNIQUE,
                user_id INTEGER,
                user_name TEXT,
                category TEXT,
                product_id TEXT,
                product_name TEXT,
                quantity INTEGER DEFAULT 1,
                price_usd REAL,
                price_stars INTEGER,
                target_recipient TEXT,
                extra_data TEXT,
                payment_method TEXT,
                status TEXT DEFAULT 'pending',
                tx_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()

def upsert_user(user_id, username=None, first_name=None, last_name=None, is_admin=0, referrer_id=None):
    with get_db() as conn:
        cursor = conn.cursor()
        # Check existing user
        cursor.execute("SELECT id, referrer_id FROM users WHERE id = ?", (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE users SET
                    username = coalesce(?, username),
                    first_name = coalesce(?, first_name),
                    last_name = coalesce(?, last_name),
                    is_admin = CASE WHEN ? = 1 THEN 1 ELSE is_admin END
                WHERE id = ?
            """, (username, first_name, last_name, is_admin, user_id))
        else:
            # New user: check if referrer is valid
            valid_ref = None
            if referrer_id and referrer_id != user_id:
                cursor.execute("SELECT id FROM users WHERE id = ?", (referrer_id,))
                if cursor.fetchone():
                    valid_ref = referrer_id

            cursor.execute("""
                INSERT INTO users (id, username, first_name, last_name, is_admin, referrer_id, balance_stars)
                VALUES (?, ?, ?, ?, ?, ?, 5000)
            """, (user_id, username, first_name, last_name, is_admin, valid_ref))

            # If valid referrer, register referral
            if valid_ref:
                try:
                    cursor.execute("""
                        INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)
                    """, (valid_ref, user_id))
                    cursor.execute("""
                        UPDATE users SET referral_count = referral_count + 1 WHERE id = ?
                    """, (valid_ref,))
                except Exception:
                    pass

        conn.commit()
        return get_user(user_id)

def get_user(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def add_balance(user_id, amount_stars, tx_type="topup", description="Top-up Stars balance"):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance_stars = balance_stars + ? WHERE id = ?", (amount_stars, user_id))
        cursor.execute("""
            INSERT INTO balance_transactions (user_id, amount_stars, type, description)
            VALUES (?, ?, ?, ?)
        """, (user_id, amount_stars, tx_type, description))
        conn.commit()
        return get_user(user_id)

def deduct_balance(user_id, amount_stars, tx_type="purchase", description="Order purchase"):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance_stars FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row or row["balance_stars"] < amount_stars:
            return False
            
        cursor.execute("UPDATE users SET balance_stars = balance_stars - ? WHERE id = ?", (amount_stars, user_id))
        cursor.execute("""
            INSERT INTO balance_transactions (user_id, amount_stars, type, description)
            VALUES (?, ?, ?, ?)
        """, (user_id, -amount_stars, tx_type, description))
        conn.commit()
        return True

def reward_referrer_commission(buyer_id, order_stars, commission_percent=5):
    """Gives commission to the buyer's referrer (5% of stars spent)."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT referrer_id FROM users WHERE id = ?", (buyer_id,))
        row = cursor.fetchone()
        if not row or not row["referrer_id"]:
            return None
            
        referrer_id = row["referrer_id"]
        commission_stars = max(1, int(order_stars * (commission_percent / 100.0)))
        
        # Credit referrer
        cursor.execute("""
            UPDATE users SET 
                balance_stars = balance_stars + ?,
                referral_earnings = referral_earnings + ?
            WHERE id = ?
        """, (commission_stars, commission_stars, referrer_id))
        
        # Update referral record
        cursor.execute("""
            UPDATE referrals SET bonus_stars = bonus_stars + ? 
            WHERE referrer_id = ? AND referred_id = ?
        """, (commission_stars, referrer_id, buyer_id))
        
        cursor.execute("""
            INSERT INTO balance_transactions (user_id, amount_stars, type, description)
            VALUES (?, ?, 'referral_bonus', ?)
        """, (referrer_id, commission_stars, f"Referral bonus from friend purchase ({order_stars} ⭐)"))
        
        conn.commit()
        return {
            "referrer_id": referrer_id,
            "commission_stars": commission_stars
        }

def get_user_referrals(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.referred_id, r.bonus_stars, r.created_at, u.username, u.first_name
            FROM referrals r
            LEFT JOIN users u ON r.referred_id = u.id
            WHERE r.referrer_id = ?
            ORDER BY r.id DESC
        """, (user_id,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_user_transactions(user_id, limit=20):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM balance_transactions WHERE user_id = ? ORDER BY id DESC LIMIT ?
        """, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

def create_order(user_id, user_name, category, product_id, product_name, quantity,
                 price_usd, price_stars, target_recipient, extra_data=None, payment_method="stars"):
    order_uuid = str(uuid.uuid4())[:8].upper()
    extra_json = json.dumps(extra_data or {})
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (
                order_uuid, user_id, user_name, category, product_id, product_name,
                quantity, price_usd, price_stars, target_recipient, extra_data,
                payment_method, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (
            order_uuid, user_id, user_name, category, product_id, product_name,
            quantity, price_usd, price_stars, target_recipient, extra_json, payment_method
        ))
        order_id = cursor.lastrowid
        conn.commit()
        return get_order(order_id)

def get_order(order_id):
    with get_db() as conn:
        cursor = conn.cursor()
        if isinstance(order_id, int):
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        else:
            cursor.execute("SELECT * FROM orders WHERE order_uuid = ?", (order_id,))
        row = cursor.fetchone()
        if row:
            d = dict(row)
            try:
                d["extra_data"] = json.loads(d["extra_data"]) if d["extra_data"] else {}
            except Exception:
                d["extra_data"] = {}
            return d
        return None

def get_user_orders(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT 50", (user_id,))
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            d = dict(row)
            try:
                d["extra_data"] = json.loads(d["extra_data"]) if d["extra_data"] else {}
            except Exception:
                d["extra_data"] = {}
            orders.append(d)
        return orders

def get_all_orders(limit=100):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        orders = []
        for row in rows:
            d = dict(row)
            try:
                d["extra_data"] = json.loads(d["extra_data"]) if d["extra_data"] else {}
            except Exception:
                d["extra_data"] = {}
            orders.append(d)
        return orders

def update_order_status(order_id, status, tx_hash=None):
    now = datetime.now().isoformat()
    with get_db() as conn:
        cursor = conn.cursor()
        if tx_hash:
            cursor.execute("""
                UPDATE orders SET status = ?, tx_hash = ?, updated_at = ? WHERE id = ? OR order_uuid = ?
            """, (status, tx_hash, now, order_id, order_id))
        else:
            cursor.execute("""
                UPDATE orders SET status = ?, updated_at = ? WHERE id = ? OR order_uuid = ?
            """, (status, now, order_id, order_id))
        conn.commit()
        return get_order(order_id)

def get_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) as total_orders, sum(price_usd) as total_usd, sum(price_stars) as total_stars FROM orders WHERE status in ('paid', 'completed')")
        summary = dict(cursor.fetchone() or {})
        cursor.execute("SELECT count(*) as pending_count FROM orders WHERE status = 'pending'")
        pending = cursor.fetchone()["pending_count"]
        cursor.execute("SELECT count(*) as total_users FROM users")
        users = cursor.fetchone()["total_users"]
        return {
            "total_orders": summary.get("total_orders") or 0,
            "total_usd": round(summary.get("total_usd") or 0.0, 2),
            "total_stars": summary.get("total_stars") or 0,
            "pending_count": pending,
            "total_users": users
        }

if __name__ == "__main__":
    init_db()
    print("Database initialized & migrated successfully.")
