# Official Product Catalog for Telegram Market Web App
# Gifts and Stars updated to match official Telegram App Gifts and pricing

CATALOG = {
    "topup_packages": [
        {"stars": 50, "price_usd": 0.99, "badge": "Starter"},
        {"stars": 100, "price_usd": 1.89, "badge": "Popular"},
        {"stars": 250, "price_usd": 4.49, "badge": "+5% Bonus"},
        {"stars": 500, "price_usd": 8.49, "badge": "Best Value"},
        {"stars": 1000, "price_usd": 15.99, "badge": "+10% Bonus"},
        {"stars": 2500, "price_usd": 36.99, "badge": "PRO Trader"},
        {"stars": 5000, "price_usd": 69.99, "badge": "VIP Whale"}
    ],
    "reactions": {
        "title": "Telegram Paid Reactions",
        "description": "Boost your channel posts with Telegram Stars paid reactions. Fast delivery, organic algorithm boost, channel monetization.",
        "icon": "⭐",
        "packages": [
            {
                "id": "react_50",
                "name": "50 Paid Stars Reactions",
                "stars_count": 50,
                "price_usd": 0.99,
                "price_stars": 50,
                "badge": "Popular",
                "delivery_time": "5-15 min",
                "description": "50 Telegram Stars distributed to your selected post."
            },
            {
                "id": "react_100",
                "name": "100 Paid Stars Reactions",
                "stars_count": 100,
                "price_usd": 1.89,
                "price_stars": 100,
                "badge": "Hot",
                "delivery_time": "5-20 min",
                "description": "100 Telegram Stars to jump-start channel engagement."
            },
            {
                "id": "react_250",
                "name": "250 Paid Stars Reactions",
                "stars_count": 250,
                "price_usd": 4.49,
                "price_stars": 250,
                "badge": "-10%",
                "delivery_time": "10-30 min",
                "description": "250 Stars reactions for viral reach on Telegram search."
            },
            {
                "id": "react_500",
                "name": "500 Paid Stars Reactions",
                "stars_count": 500,
                "price_usd": 8.49,
                "price_stars": 500,
                "badge": "Best Value",
                "delivery_time": "15-45 min",
                "description": "500 Stars reactions to dominate Telegram post rankings."
            },
            {
                "id": "react_1000",
                "name": "1,000 Paid Stars Reactions",
                "stars_count": 1000,
                "price_usd": 15.99,
                "price_stars": 1000,
                "badge": "-20%",
                "delivery_time": "30-60 min",
                "description": "1,000 Stars reactions for major announcements & giveaways."
            },
            {
                "id": "react_2500",
                "name": "2,500 Paid Stars Reactions",
                "stars_count": 2500,
                "price_usd": 36.99,
                "price_stars": 2500,
                "badge": "PRO",
                "delivery_time": "1-2 hours",
                "description": "2,500 Stars for maximum channel monetization & visibility."
            },
            {
                "id": "react_5000",
                "name": "5,000 Paid Stars Reactions",
                "stars_count": 5000,
                "price_usd": 69.99,
                "price_stars": 5000,
                "badge": "ULTRA",
                "delivery_time": "1-3 hours",
                "description": "5,000 Stars reactions package for elite channels & brands."
            }
        ],
        "emoji_options": [
            {"emoji": "⭐", "name": "Star", "color": "#ffbe0b"},
            {"emoji": "🔥", "name": "Fire", "color": "#ff5400"},
            {"emoji": "❤️", "name": "Heart", "color": "#ff0054"},
            {"emoji": "👍", "name": "Thumbs Up", "color": "#48cae4"},
            {"emoji": "🚀", "name": "Rocket", "color": "#7209b7"},
            {"emoji": "🎉", "name": "Party", "color": "#f72585"},
            {"emoji": "👏", "name": "Applause", "color": "#ffd166"},
            {"emoji": "🏆", "name": "Trophy", "color": "#ffb703"},
            {"emoji": "💎", "name": "Diamond", "color": "#00b4d8"},
            {"emoji": "⚡", "name": "Lightning", "color": "#fee440"}
        ]
    },
    "premium": {
        "title": "Telegram Premium",
        "description": "Upgrade any account or gift Telegram Premium without needing bank cards. Instant activation.",
        "icon": "💎",
        "packages": [
            {
                "id": "prem_3m",
                "name": "3 Months Premium",
                "duration_months": 3,
                "price_usd": 11.99,
                "price_stars": 600,
                "badge": "Entry",
                "savings": "Save 15%",
                "description": "3 Months of full Telegram Premium unlocked on recipient profile."
            },
            {
                "id": "prem_6m",
                "name": "6 Months Premium",
                "duration_months": 6,
                "price_usd": 16.99,
                "price_stars": 850,
                "badge": "Popular",
                "savings": "Save 25%",
                "description": "6 Months Telegram Premium gift delivered directly to Telegram account."
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
        "description": "Official Telegram collectible profile gifts. Can be displayed on profile or converted into Stars.",
        "icon": "🎁",
        "packages": [
            {
                "id": "gift_star",
                "name": "Green Star",
                "emoji": "⭐",
                "stars_value": 15,
                "price_usd": 0.35,
                "price_stars": 15,
                "badge": "Official 15 ⭐",
                "glow_color": "#2ec4b6",
                "description": "Official Telegram Mini Star gift to show appreciation."
            },
            {
                "id": "gift_cake",
                "name": "Delicious Cake",
                "emoji": "🎂",
                "stars_value": 25,
                "price_usd": 0.59,
                "price_stars": 25,
                "badge": "Official 25 ⭐",
                "glow_color": "#ff758f",
                "description": "Celebratory birthday or greeting cake with sparkling candles."
            },
            {
                "id": "gift_heart",
                "name": "Red Heart",
                "emoji": "❤️",
                "stars_value": 50,
                "price_usd": 1.19,
                "price_stars": 50,
                "badge": "Official 50 ⭐",
                "glow_color": "#ff0054",
                "description": "Classic red heart collectible for someone special."
            },
            {
                "id": "gift_rocket",
                "name": "Space Rocket",
                "emoji": "🚀",
                "stars_value": 100,
                "price_usd": 2.29,
                "price_stars": 100,
                "badge": "Official 100 ⭐",
                "glow_color": "#7b2cbf",
                "description": "To the moon! Cosmic rocket gift for tech and crypto enthusiasts."
            },
            {
                "id": "gift_rose",
                "name": "Velvet Rose",
                "emoji": "🌹",
                "stars_value": 100,
                "price_usd": 2.29,
                "price_stars": 100,
                "badge": "Official 100 ⭐",
                "glow_color": "#d90429",
                "description": "Silky crimson blooming rose for romantic and elegant occasions."
            },
            {
                "id": "gift_trophy",
                "name": "Golden Trophy",
                "emoji": "🏆",
                "stars_value": 100,
                "price_usd": 2.29,
                "price_stars": 100,
                "badge": "Official 100 ⭐",
                "glow_color": "#ffb703",
                "description": "Polished gold trophy cup for winners, milestones and achievements."
            },
            {
                "id": "gift_kiss",
                "name": "Heart Box",
                "emoji": "💝",
                "stars_value": 150,
                "price_usd": 3.49,
                "price_stars": 150,
                "badge": "Official 150 ⭐",
                "glow_color": "#ff4d6d",
                "description": "Ribbon-wrapped heart gift box filled with affection."
            },
            {
                "id": "gift_bear",
                "name": "Plush Bear",
                "emoji": "🧸",
                "stars_value": 250,
                "price_usd": 5.79,
                "price_stars": 250,
                "badge": "Official 250 ⭐",
                "glow_color": "#fb8500",
                "description": "Adorable plush teddy bear wearing an embroidered bow."
            },
            {
                "id": "gift_wand",
                "name": "Magic Wand",
                "emoji": "🪄",
                "stars_value": 350,
                "price_usd": 7.99,
                "price_stars": 350,
                "badge": "Official 350 ⭐",
                "glow_color": "#a29bfe",
                "description": "Enchanted glowing wand sparkling with magical stardust."
            },
            {
                "id": "gift_champagne",
                "name": "Sparkling Champagne",
                "emoji": "🍾",
                "stars_value": 500,
                "price_usd": 11.49,
                "price_stars": 500,
                "badge": "Official 500 ⭐",
                "glow_color": "#ffd166",
                "description": "Luxury effervescent champagne bottle popped for big victories."
            },
            {
                "id": "gift_diamond",
                "name": "Royal Diamond",
                "emoji": "💎",
                "stars_value": 1000,
                "price_usd": 22.99,
                "price_stars": 1000,
                "badge": "Official 1000 ⭐",
                "glow_color": "#00b4d8",
                "description": "Brilliant multi-faceted luxury diamond with prismatic reflections."
            },
            {
                "id": "gift_crown",
                "name": "Imperial Crown",
                "emoji": "👑",
                "stars_value": 2500,
                "price_usd": 54.99,
                "price_stars": 2500,
                "badge": "Official 2500 ⭐",
                "glow_color": "#9d4edd",
                "description": "The ultimate VIP status symbol on Telegram profiles."
            }
        ]
    }
}
