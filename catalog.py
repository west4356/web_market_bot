# Official Product Catalog for Telegram Market Web App
# Stars (min 50 Stars Fragment-style), Telegram Premium (3m, 6m, 1y), and Gifts (15 to 100 Stars)

CATALOG = {
    "topup_packages": [
        {"stars": 50, "price_usd": 0.99, "badge": "Starter (Min)"},
        {"stars": 100, "price_usd": 1.89, "badge": "Popular"},
        {"stars": 250, "price_usd": 4.49, "badge": "+5% Bonus"},
        {"stars": 500, "price_usd": 8.49, "badge": "Best Value"},
        {"stars": 1000, "price_usd": 15.99, "badge": "+10% Bonus"},
        {"stars": 2500, "price_usd": 36.99, "badge": "PRO Trader"},
        {"stars": 5000, "price_usd": 69.99, "badge": "VIP Whale"}
    ],
    "stars": {
        "title": "Buy Telegram Stars",
        "description": "Buy Telegram Stars directly to your Telegram ID account (Fragment style). Minimum 50 Stars.",
        "icon": "⭐",
        "min_stars": 50,
        "packages": [
            {
                "id": "stars_50",
                "name": "50 Telegram Stars",
                "stars_count": 50,
                "price_usd": 0.99,
                "price_stars": 50,
                "badge": "Min 50 ⭐",
                "delivery_time": "Instant ⚡",
                "description": "50 Telegram Stars deposited directly to your Telegram ID account balance."
            },
            {
                "id": "stars_100",
                "name": "100 Telegram Stars",
                "stars_count": 100,
                "price_usd": 1.89,
                "price_stars": 100,
                "badge": "Popular",
                "delivery_time": "Instant ⚡",
                "description": "100 Telegram Stars deposited directly to your Telegram ID account balance."
            },
            {
                "id": "stars_250",
                "name": "250 Telegram Stars",
                "stars_count": 250,
                "price_usd": 4.49,
                "price_stars": 250,
                "badge": "+5% Bonus",
                "delivery_time": "Instant ⚡",
                "description": "250 Telegram Stars deposited directly to your Telegram ID account balance."
            },
            {
                "id": "stars_500",
                "name": "500 Telegram Stars",
                "stars_count": 500,
                "price_usd": 8.49,
                "price_stars": 500,
                "badge": "Best Value",
                "delivery_time": "Instant ⚡",
                "description": "500 Telegram Stars deposited directly to your Telegram ID account balance."
            },
            {
                "id": "stars_1000",
                "name": "1,000 Telegram Stars",
                "stars_count": 1000,
                "price_usd": 15.99,
                "price_stars": 1000,
                "badge": "+10% Bonus",
                "delivery_time": "Instant ⚡",
                "description": "1,000 Telegram Stars deposited directly to your Telegram ID account balance."
            },
            {
                "id": "stars_2500",
                "name": "2,500 Telegram Stars",
                "stars_count": 2500,
                "price_usd": 36.99,
                "price_stars": 2500,
                "badge": "PRO",
                "delivery_time": "Instant ⚡",
                "description": "2,500 Telegram Stars deposited directly to your Telegram ID account balance."
            },
            {
                "id": "stars_5000",
                "name": "5,000 Telegram Stars",
                "stars_count": 5000,
                "price_usd": 69.99,
                "price_stars": 5000,
                "badge": "VIP Whale",
                "delivery_time": "Instant ⚡",
                "description": "5,000 Telegram Stars deposited directly to your Telegram ID account balance."
            }
        ]
    },
    "premium": {
        "title": "Telegram Premium Subscriptions",
        "description": "Upgrade your Telegram account or gift Telegram Premium (3, 6, or 12 months) via Telegram payments. Instant activation without bank cards.",
        "icon": "💎",
        "packages": [
            {
                "id": "prem_3m",
                "name": "3 Months Premium",
                "duration_months": 3,
                "price_usd": 11.99,
                "price_stars": 600,
                "badge": "3 Months",
                "savings": "Save 15%",
                "description": "3 Months full Telegram Premium subscription unlocked on your Telegram account."
            },
            {
                "id": "prem_6m",
                "name": "6 Months Premium",
                "duration_months": 6,
                "price_usd": 16.99,
                "price_stars": 850,
                "badge": "Popular",
                "savings": "Save 25%",
                "description": "6 Months Telegram Premium subscription delivered directly to your Telegram account."
            },
            {
                "id": "prem_12m",
                "name": "12 Months (1 Year) Premium",
                "duration_months": 12,
                "price_usd": 28.99,
                "price_stars": 1450,
                "badge": "Best Deal",
                "savings": "Save 45%",
                "description": "Full 1 Year Telegram Premium subscription with maximum discount."
            }
        ],
        "features": [
            {"icon": "📁", "title": "4 GB File Uploads", "desc": "Upload videos and documents up to 4 GB each"},
            {"icon": "⚡", "title": "Faster Download Speed", "desc": "Download media at maximum possible network speed"},
            {"icon": "🎙️", "title": "Voice-to-Text", "desc": "Read transcripts of any voice message or video message"},
            {"icon": "🚫", "title": "No Advertisements", "desc": "Completely ad-free experience in public channels"},
            {"icon": "✨", "title": "Animated Emoji Reactions", "desc": "React with thousands of exclusive animated emoji"},
            {"icon": "⭐", "title": "Premium Badge", "desc": "Star icon next to your name indicating your status"},
            {"icon": "🎨", "title": "Custom App Icons & Colors", "desc": "Personalize your chat background and app launcher icon"},
            {"icon": "📈", "title": "Doubled Limits", "desc": "Follow up to 1,000 channels, 30 chat folders, 10 pins"}
        ]
    },
    "gifts": {
        "title": "Telegram Gifts",
        "description": "Official Telegram collectible profile gifts (15 to 100 Stars). Buy to your account or send to friends!",
        "icon": "🎁",
        "min_stars": 15,
        "max_stars": 100,
        "packages": [
            {
                "id": "gift_heart",
                "name": "Heart",
                "emoji": "❤️",
                "stars_value": 15,
                "price_usd": 0.35,
                "price_stars": 15,
                "badge": "15 ⭐",
                "glow_color": "#ff0054",
                "description": "Telegram Heart Collectible Profile Gift."
            },
            {
                "id": "gift_bear",
                "name": "Plush Bear",
                "emoji": "🧸",
                "stars_value": 15,
                "price_usd": 0.35,
                "price_stars": 15,
                "badge": "15 ⭐",
                "glow_color": "#fb8500",
                "description": "Adorable Plush Bear Collectible Gift."
            },
            {
                "id": "gift_star",
                "name": "Golden Star",
                "emoji": "⭐",
                "stars_value": 15,
                "price_usd": 0.35,
                "price_stars": 15,
                "badge": "15 ⭐",
                "glow_color": "#ffbe0b",
                "description": "Shining Golden Star Profile Collectible."
            },
            {
                "id": "gift_box",
                "name": "Gift Box",
                "emoji": "🎁",
                "stars_value": 25,
                "price_usd": 0.59,
                "price_stars": 25,
                "badge": "25 ⭐",
                "glow_color": "#ff4d6d",
                "description": "Festive Wrapped Gift Box."
            },
            {
                "id": "gift_rose",
                "name": "Rose",
                "emoji": "🌹",
                "stars_value": 25,
                "price_usd": 0.59,
                "price_stars": 25,
                "badge": "25 ⭐",
                "glow_color": "#d90429",
                "description": "Silky Crimson Blooming Rose."
            },
            {
                "id": "gift_cake",
                "name": "Birthday Cake",
                "emoji": "🎂",
                "stars_value": 50,
                "price_usd": 1.19,
                "price_stars": 50,
                "badge": "50 ⭐",
                "glow_color": "#ff758f",
                "description": "Celebratory Birthday Cake with Candles."
            },
            {
                "id": "gift_bouquet",
                "name": "Bouquet",
                "emoji": "💐",
                "stars_value": 50,
                "price_usd": 1.19,
                "price_stars": 50,
                "badge": "50 ⭐",
                "glow_color": "#a29bfe",
                "description": "Vibrant Bouquet of Fresh Flowers."
            },
            {
                "id": "gift_rocket",
                "name": "Rocket",
                "emoji": "🚀",
                "stars_value": 50,
                "price_usd": 1.19,
                "price_stars": 50,
                "badge": "50 ⭐",
                "glow_color": "#7b2cbf",
                "description": "Cosmic Space Rocket Profile Gift."
            },
            {
                "id": "gift_champagne",
                "name": "Champagne",
                "emoji": "🍾",
                "stars_value": 50,
                "price_usd": 1.19,
                "price_stars": 50,
                "badge": "50 ⭐",
                "glow_color": "#ffd166",
                "description": "Sparkling Popped Champagne for Celebrations."
            },
            {
                "id": "gift_fire",
                "name": "Fire Trophy",
                "emoji": "🔥",
                "stars_value": 75,
                "price_usd": 1.75,
                "price_stars": 75,
                "badge": "75 ⭐",
                "glow_color": "#ff5400",
                "description": "Blazing Fire Trophy Collectible Gift."
            },
            {
                "id": "gift_crystal",
                "name": "Magic Crystal",
                "emoji": "🔮",
                "stars_value": 75,
                "price_usd": 1.75,
                "price_stars": 75,
                "badge": "75 ⭐",
                "glow_color": "#9d4edd",
                "description": "Mystical Radiant Crystal Ball Gift."
            },
            {
                "id": "gift_cup",
                "name": "Champions Cup",
                "emoji": "🏆",
                "stars_value": 100,
                "price_usd": 2.29,
                "price_stars": 100,
                "badge": "100 ⭐",
                "glow_color": "#ffb703",
                "description": "Golden Champions Trophy Cup."
            },
            {
                "id": "gift_ring",
                "name": "Diamond Ring",
                "emoji": "💍",
                "stars_value": 100,
                "price_usd": 2.29,
                "price_stars": 100,
                "badge": "100 ⭐",
                "glow_color": "#48cae4",
                "description": "Precious Sparkling Diamond Ring."
            },
            {
                "id": "gift_diamond",
                "name": "Diamond",
                "emoji": "💎",
                "stars_value": 100,
                "price_usd": 2.29,
                "price_stars": 100,
                "badge": "100 ⭐",
                "glow_color": "#00b4d8",
                "description": "Brilliant Radiant Luxury Diamond Gift."
            }
        ]
    }
}
