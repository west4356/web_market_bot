// Telegram Web App Market Application Logic

const tg = window.Telegram?.WebApp || null;

// Embedded Fallback Catalog to guarantee instant rendering
const DEFAULT_CATALOG = {
  stars: {
    title: "Buy Telegram Stars",
    description: "Deposit Telegram Stars directly to your Telegram ID account (Fragment style). Minimum 50 Stars.",
    icon: "⭐",
    min_stars: 50,
    packages: [
      { id: "stars_50", name: "50 Telegram Stars", stars_count: 50, price_usd: 0.99, price_stars: 50, badge: "Min 50 ⭐", delivery_time: "Instant ⚡", description: "50 Stars deposited directly to your Telegram ID account." },
      { id: "stars_100", name: "100 Telegram Stars", stars_count: 100, price_usd: 1.89, price_stars: 100, badge: "Popular", delivery_time: "Instant ⚡", description: "100 Stars deposited directly to your Telegram ID account." },
      { id: "stars_250", name: "250 Telegram Stars", stars_count: 250, price_usd: 4.49, price_stars: 250, badge: "+5% Bonus", delivery_time: "Instant ⚡", description: "250 Stars deposited directly to your Telegram ID account." },
      { id: "stars_500", name: "500 Telegram Stars", stars_count: 500, price_usd: 8.49, price_stars: 500, badge: "Best Value", delivery_time: "Instant ⚡", description: "500 Stars deposited directly to your Telegram ID account." },
      { id: "stars_1000", name: "1,000 Telegram Stars", stars_count: 1000, price_usd: 15.99, price_stars: 1000, badge: "+10% Bonus", delivery_time: "Instant ⚡", description: "1,000 Stars deposited directly to your Telegram ID account." },
      { id: "stars_2500", name: "2,500 Telegram Stars", stars_count: 2500, price_usd: 36.99, price_stars: 2500, badge: "PRO", delivery_time: "Instant ⚡", description: "2,500 Stars deposited directly to your Telegram ID account." },
      { id: "stars_5000", name: "5,000 Telegram Stars", stars_count: 5000, price_usd: 69.99, price_stars: 5000, badge: "VIP Whale", delivery_time: "Instant ⚡", description: "5,000 Stars deposited directly to your Telegram ID account." }
    ]
  },
  premium: {
    title: "Telegram Premium Subscriptions",
    description: "Activate 3, 6, or 12 months (1 year) Telegram Premium subscriptions with instant Telegram payments.",
    icon: "💎",
    packages: [
      { id: "prem_3m", name: "3 Months Premium", duration_months: 3, price_usd: 11.99, price_stars: 600, badge: "3 Months", savings: "Save 15%", description: "3 Months of full Telegram Premium unlocked on recipient profile." },
      { id: "prem_6m", name: "6 Months Premium", duration_months: 6, price_usd: 16.99, price_stars: 850, badge: "Popular", savings: "Save 25%", description: "6 Months Telegram Premium subscription delivered directly to Telegram account." },
      { id: "prem_12m", name: "12 Months (1 Year) Premium", duration_months: 12, price_usd: 28.99, price_stars: 1450, badge: "Best Deal", savings: "Save 45%", description: "Full 1 Year Telegram Premium subscription with maximum discount." }
    ],
    features: [
      { icon: "📁", title: "4 GB File Uploads", desc: "Upload videos and documents up to 4 GB each" },
      { icon: "⚡", title: "Faster Download Speed", desc: "Download media at maximum possible network speed" },
      { icon: "🎙️", title: "Voice-to-Text", desc: "Read transcripts of any voice message or video message" },
      { icon: "🚫", title: "No Advertisements", desc: "Completely ad-free experience in public channels" },
      { icon: "✨", title: "Animated Emoji Reactions", desc: "React with thousands of exclusive animated emoji" },
      { icon: "⭐", title: "Premium Badge", desc: "Star icon next to your name indicating your status" },
      { icon: "🎨", title: "Custom App Icons & Colors", desc: "Personalize your chat background and app launcher icon" },
      { icon: "📈", title: "Doubled Limits", desc: "Follow up to 1,000 channels, 30 chat folders, 10 pins" }
    ]
  },
  gifts: {
    title: "Telegram Gifts",
    description: "Official Telegram collectible profile gifts (15 to 100 Stars, nothing more).",
    icon: "🎁",
    packages: [
      { id: "gift_heart", name: "Heart", emoji: "❤️", stars_value: 15, price_usd: 0.35, price_stars: 15, badge: "15 ⭐", glow_color: "#ff0054", description: "Telegram Heart Profile Gift." },
      { id: "gift_bear", name: "Plush Bear", emoji: "🧸", stars_value: 15, price_usd: 0.35, price_stars: 15, badge: "15 ⭐", glow_color: "#fb8500", description: "Adorable Plush Bear Collectible." },
      { id: "gift_star", name: "Golden Star", emoji: "⭐", stars_value: 15, price_usd: 0.35, price_stars: 15, badge: "15 ⭐", glow_color: "#ffbe0b", description: "Golden Star Profile Collectible." },
      { id: "gift_box", name: "Gift Box", emoji: "🎁", stars_value: 25, price_usd: 0.59, price_stars: 25, badge: "25 ⭐", glow_color: "#ff4d6d", description: "Festive Wrapped Gift Box." },
      { id: "gift_rose", name: "Rose", emoji: "🌹", stars_value: 25, price_usd: 0.59, price_stars: 25, badge: "25 ⭐", glow_color: "#d90429", description: "Silky Crimson Blooming Rose." },
      { id: "gift_cake", name: "Birthday Cake", emoji: "🎂", stars_value: 50, price_usd: 1.19, price_stars: 50, badge: "50 ⭐", glow_color: "#ff758f", description: "Celebratory Birthday Cake." },
      { id: "gift_bouquet", name: "Bouquet", emoji: "💐", stars_value: 50, price_usd: 1.19, price_stars: 50, badge: "50 ⭐", glow_color: "#a29bfe", description: "Fresh Flower Bouquet." },
      { id: "gift_rocket", name: "Rocket", emoji: "🚀", stars_value: 50, price_usd: 1.19, price_stars: 50, badge: "50 ⭐", glow_color: "#7b2cbf", description: "Cosmic Rocket Profile Gift." },
      { id: "gift_champagne", name: "Champagne", emoji: "🍾", stars_value: 50, price_usd: 1.19, price_stars: 50, badge: "50 ⭐", glow_color: "#ffd166", description: "Popped Champagne for Celebrations." },
      { id: "gift_fire", name: "Fire Trophy", emoji: "🔥", stars_value: 75, price_usd: 1.75, price_stars: 75, badge: "75 ⭐", glow_color: "#ff5400", description: "Blazing Fire Collectible Gift." },
      { id: "gift_crystal", name: "Magic Crystal", emoji: "🔮", stars_value: 75, price_usd: 1.75, price_stars: 75, badge: "75 ⭐", glow_color: "#9d4edd", description: "Mystical Radiant Crystal Ball." },
      { id: "gift_cup", name: "Champions Cup", emoji: "🏆", stars_value: 100, price_usd: 2.29, price_stars: 100, badge: "100 ⭐", glow_color: "#ffb703", description: "Golden Champions Trophy Cup." },
      { id: "gift_ring", name: "Diamond Ring", emoji: "💍", stars_value: 100, price_usd: 2.29, price_stars: 100, badge: "100 ⭐", glow_color: "#48cae4", description: "Precious Sparkling Diamond Ring." },
      { id: "gift_diamond", name: "Diamond", emoji: "💎", stars_value: 100, price_usd: 2.29, price_stars: 100, badge: "100 ⭐", glow_color: "#00b4d8", description: "Brilliant Luxury Diamond Gift." }
    ]
  },
  topup_packages: [
    { stars: 50, price_usd: 0.99, badge: "Min 50 ⭐" },
    { stars: 100, price_usd: 1.89, badge: "Popular" },
    { stars: 250, price_usd: 4.49, badge: "+5% Bonus" },
    { stars: 500, price_usd: 8.49, badge: "Best Value" },
    { stars: 1000, price_usd: 15.99, badge: "+10% Bonus" },
    { stars: 2500, price_usd: 36.99, badge: "PRO" },
    { stars: 5000, price_usd: 69.99, badge: "VIP" }
  ]
};

// Application State
const state = {
  user: {
    id: 12345678,
    first_name: "Telegram User",
    username: "",
    balance_stars: 0,
    referral_count: 0,
    referral_earnings: 0,
    language_code: "en"
  },
  activeTab: "stars",
  catalog: DEFAULT_CATALOG,
  config: null,
  isAdmin: false,
  referralLink: "",
  
  // Selection states
  stars: {
    selectedPackage: null,
    customStars: null,
    targetUser: ""
  },
  premium: {
    selectedPackage: null,
    targetUser: ""
  },
  gifts: {
    selectedGift: null,
    targetUser: "",
    message: "",
    isAnonymous: false
  },
  
  // Top-Up selection
  topup: {
    selectedStars: 50
  },
  
  // Checkout
  checkout: {
    item: null,
    paymentMethod: "stars"
  }
};

// Multilingual Dictionary
const i18n = {
  en: {
    tab_stars: "Buy Stars",
    tab_premium: "Premium",
    tab_gifts: "Gifts (15-100⭐)",
    tab_referrals: "Referrals",
    tab_orders: "Orders",
    label_recipient: "Recipient Telegram ID or Username",
    select_duration: "Select Subscription Duration",
    label_gift_recipient: "Recipient Telegram ID or Username",
    choose_gift: "Choose a Collectible Gift (15 ⭐ - 100 ⭐)",
    btn_order_stars: "Buy Stars to Account",
    btn_order_premium: "Buy Telegram Premium",
    btn_order_gift: "Send Telegram Gift",
    proceed_to_pay: "Proceed to Pay",
    username_required: "Please enter a recipient Telegram ID or username!"
  },
  ru: {
    tab_stars: "Купить Звёзды",
    tab_premium: "Премиум",
    tab_gifts: "Подарки (15-100⭐)",
    tab_referrals: "Рефералы",
    tab_orders: "Заказы",
    label_recipient: "Telegram ID или юзернейм",
    select_duration: "Срок подписки",
    label_gift_recipient: "Telegram ID или юзернейм",
    choose_gift: "Выберите подарок (от 15 до 100 ⭐)",
    btn_order_stars: "Купить Звёзды на аккаунт",
    btn_order_premium: "Купить Telegram Premium",
    btn_order_gift: "Отправить подарок",
    proceed_to_pay: "Оплатить заказ",
    username_required: "Пожалуйста, введите Telegram ID или юзернейм!"
  },
  uz: {
    tab_stars: "Yulduzlar olish",
    tab_premium: "Premium",
    tab_gifts: "Sovg'alar (15-100⭐)",
    tab_referrals: "Referallar",
    tab_orders: "Buyurtmalar",
    label_recipient: "Telegram ID yoki username",
    select_duration: "Obuna muddatini tanlang",
    label_gift_recipient: "Telegram ID yoki username",
    choose_gift: "Sovg'ani tanlang (15 dan 100 ⭐ gacha)",
    btn_order_stars: "Akkauntga yulduzlar olish",
    btn_order_premium: "Telegram Premium sotib olish",
    btn_order_gift: "Sovg'a yuborish",
    proceed_to_pay: "To'lovni amalga oshirish",
    username_required: "Iltimos, Telegram ID yoki usernameni kiriting!"
  }
};

let currentLang = "en";

// Haptic Feedback Helper
function haptic(type = "light") {
  if (tg?.HapticFeedback) {
    if (type === "light" || type === "medium" || type === "heavy") {
      tg.HapticFeedback.impactOccurred(type);
    } else if (type === "success" || type === "error" || type === "warning") {
      tg.HapticFeedback.notificationOccurred(type);
    }
  }
}

// Show Toast Notification
function showToast(msg) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 3200);
}

// Helper to get self recipient string
function getSelfRecipient() {
  if (state.user.username) {
    return state.user.username.startsWith("@") ? state.user.username : `@${state.user.username}`;
  }
  return `ID: ${state.user.id}`;
}

// Initialize Application
document.addEventListener("DOMContentLoaded", async () => {
  // Init Telegram SDK
  if (tg) {
    try {
      tg.ready();
      tg.expand();
      if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        state.user = { ...state.user, ...tg.initDataUnsafe.user };
      }
    } catch (e) {
      console.warn("Telegram WebApp init warning:", e);
    }
  }

  updateUserProfile();
  setupNavigation();
  setupLanguageSwitcher();
  setupInputs();
  setupCheckoutModal();
  setupTopupModal();

  // Instant render with default catalog
  renderStarsTab();
  renderPremiumTab();
  renderGiftsTab();
  renderTopupPackages();

  // Load backend catalog & user profile
  await Promise.all([
    fetchAppData(),
    fetchUserProfile()
  ]);

  // Re-render with backend data
  renderStarsTab();
  renderPremiumTab();
  renderGiftsTab();
  renderTopupPackages();
  loadUserOrders();
});

// Update Profile & Balance in Header
function updateUserProfile() {
  const userNameEl = document.getElementById("userName");
  const userHandleEl = document.getElementById("userHandle");
  const avatarEl = document.getElementById("userAvatar");
  const balanceEl = document.getElementById("headerBalanceAmount");

  if (state.user) {
    if (userNameEl) userNameEl.textContent = state.user.first_name || "Telegram User";
    if (userHandleEl) userHandleEl.textContent = state.user.username ? `@${state.user.username}` : `ID: ${state.user.id}`;
    if (avatarEl) avatarEl.textContent = (state.user.first_name || "T")[0].toUpperCase();
    if (balanceEl) balanceEl.textContent = state.user.balance_stars || 0;
  }
}

// Setup Navigation Tabs
function setupNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const tabName = tab.getAttribute("data-tab");
      switchTab(tabName);
    });
  });

  const adminToggleBtn = document.getElementById("adminToggleBtn");
  if (adminToggleBtn) {
    adminToggleBtn.addEventListener("click", () => {
      haptic("medium");
      switchTab("admin");
      loadAdminDashboard();
    });
  }

  const closeAdminBtn = document.getElementById("closeAdminBtn");
  if (closeAdminBtn) {
    closeAdminBtn.addEventListener("click", () => {
      switchTab("stars");
    });
  }

  const refreshOrdersBtn = document.getElementById("refreshOrdersBtn");
  if (refreshOrdersBtn) {
    refreshOrdersBtn.addEventListener("click", () => {
      haptic("light");
      loadUserOrders();
    });
  }
}

function switchTab(tabName) {
  haptic("light");
  state.activeTab = tabName;

  document.querySelectorAll(".nav-tab").forEach((t) => {
    t.classList.toggle("active", t.getAttribute("data-tab") === tabName);
  });

  document.querySelectorAll(".tab-content").forEach((c) => {
    c.classList.remove("active");
  });

  const activeContent = document.getElementById(`tab-${tabName}`);
  if (activeContent) {
    activeContent.classList.add("active");
  }

  // Telegram BackButton management
  if (tg?.BackButton) {
    if (tabName === "admin") {
      tg.BackButton.show();
      tg.BackButton.onClick(() => switchTab("stars"));
    } else {
      tg.BackButton.hide();
    }
  }
}

// Language Switcher
function setupLanguageSwitcher() {
  const langSelect = document.getElementById("langSelect");
  if (langSelect) {
    langSelect.addEventListener("change", (e) => {
      currentLang = e.target.value;
      haptic("light");
      applyTranslations();
    });
  }
}

function applyTranslations() {
  const dict = i18n[currentLang] || i18n.en;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });
}

// Fetch Catalog & Config
async function fetchAppData() {
  try {
    const [catRes, cfgRes] = await Promise.all([
      fetch("/api/catalog").then((r) => r.json()).catch(() => null),
      fetch("/api/config").then((r) => r.json()).catch(() => null)
    ]);

    if (catRes && catRes.ok && catRes.catalog) {
      state.catalog = catRes.catalog;
    }
    if (cfgRes) {
      state.config = cfgRes;
      if (cfgRes.admin_ids && cfgRes.admin_ids.includes(state.user.id)) {
        state.isAdmin = true;
        const btn = document.getElementById("adminToggleBtn");
        if (btn) btn.style.display = "block";
      }
    }
  } catch (err) {
    console.error("Failed to fetch app data:", err);
  }
}

// Fetch User Profile & Referral Data
async function fetchUserProfile() {
  try {
    const res = await fetch(`/api/user/${state.user.id}`);
    const data = await res.json();
    if (data.ok && data.user) {
      state.user.balance_stars = data.user.balance_stars || 0;
      state.user.referral_count = data.user.referral_count || 0;
      state.user.referral_earnings = data.user.referral_earnings || 0;
      state.referralLink = data.referral_link || `https://t.me/vst_starsmarket_bot?start=ref_${state.user.id}`;

      updateUserProfile();

      const refInput = document.getElementById("refLinkInput");
      if (refInput) refInput.value = state.referralLink;
      const refCountEl = document.getElementById("refCount");
      if (refCountEl) refCountEl.textContent = state.user.referral_count;
      const refEarnEl = document.getElementById("refEarnings");
      if (refEarnEl) refEarnEl.textContent = `${state.user.referral_earnings} ⭐`;
    }
  } catch (err) {
    console.error("Failed to fetch user profile:", err);
  }
}

// ================= TAB 1: BUY TELEGRAM STARS (MIN 50 STARS FRAGMENT STYLE) =================
function renderStarsTab() {
  const data = state.catalog?.stars;
  if (!data || !data.packages) return;

  const pkgGrid = document.getElementById("starsPackagesGrid");
  if (!pkgGrid) return;
  pkgGrid.innerHTML = "";

  data.packages.forEach((pkg, index) => {
    const card = document.createElement("div");
    card.className = `package-card ${index === 0 ? "selected" : ""}`;
    card.innerHTML = `
      ${pkg.badge ? `<div class="package-badge">${pkg.badge}</div>` : ""}
      <div class="package-stars">⭐ ${pkg.stars_count}</div>
      <div class="package-price">$${pkg.price_usd.toFixed(2)}</div>
      <div class="package-time">⚡ ${pkg.delivery_time || "Instant"}</div>
    `;

    card.addEventListener("click", () => {
      haptic("medium");
      document.querySelectorAll("#starsPackagesGrid .package-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      state.stars.selectedPackage = pkg;
      state.stars.customStars = null;
      const customInput = document.getElementById("customStarsInput");
      if (customInput) customInput.value = "";
      const customPriceTag = document.getElementById("customPriceTag");
      if (customPriceTag) customPriceTag.textContent = "$0.00";
      updateStarsButton();
    });

    pkgGrid.appendChild(card);
  });

  state.stars.selectedPackage = data.packages[0];
  updateStarsButton();
}

function updateStarsButton() {
  const priceTag = document.getElementById("starsBtnPrice");
  if (!priceTag) return;
  if (state.stars.customStars) {
    const priceUsd = (state.stars.customStars * 0.016).toFixed(2);
    priceTag.textContent = `$${priceUsd}`;
  } else if (state.stars.selectedPackage) {
    const pkg = state.stars.selectedPackage;
    priceTag.textContent = `$${pkg.price_usd.toFixed(2)}`;
  }
}

// ================= TAB 2: TELEGRAM PREMIUM (3m, 6m, 1y) =================
function renderPremiumTab() {
  const data = state.catalog?.premium;
  if (!data || !data.packages) return;

  const pkgGrid = document.getElementById("premiumPackagesGrid");
  if (!pkgGrid) return;
  pkgGrid.innerHTML = "";

  data.packages.forEach((pkg, index) => {
    const card = document.createElement("div");
    card.className = `premium-card ${index === 1 ? "selected" : ""}`;
    card.innerHTML = `
      <div class="prem-left">
        <div class="prem-duration">
          <span>${pkg.name}</span>
          ${pkg.savings ? `<span class="prem-savings">${pkg.savings}</span>` : ""}
        </div>
        <div class="prem-desc">${pkg.description}</div>
      </div>
      <div class="prem-right">
        <div class="prem-price">$${pkg.price_usd.toFixed(2)}</div>
        <div class="prem-stars">${pkg.price_stars} ⭐</div>
      </div>
    `;

    card.addEventListener("click", () => {
      haptic("medium");
      document.querySelectorAll(".premium-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      state.premium.selectedPackage = pkg;
      const priceTag = document.getElementById("premBtnPrice");
      if (priceTag) priceTag.textContent = `$${pkg.price_usd.toFixed(2)}`;
    });

    pkgGrid.appendChild(card);
  });

  state.premium.selectedPackage = data.packages[1];

  const perksGrid = document.getElementById("perksGrid");
  if (perksGrid && data.features) {
    perksGrid.innerHTML = "";
    data.features.forEach((f) => {
      const item = document.createElement("div");
      item.className = "perk-item";
      item.innerHTML = `
        <div class="perk-header">
          <span>${f.icon}</span>
          <span>${f.title}</span>
        </div>
        <div class="perk-desc">${f.desc}</div>
      `;
      perksGrid.appendChild(item);
    });
  }
}

// ================= TAB 3: TELEGRAM GIFTS (15 TO 100 STARS) =================
function renderGiftsTab() {
  const data = state.catalog?.gifts;
  if (!data || !data.packages) return;

  const giftsGrid = document.getElementById("giftsGrid");
  if (!giftsGrid) return;
  giftsGrid.innerHTML = "";

  data.packages.forEach((gift, index) => {
    const card = document.createElement("div");
    card.className = `gift-card ${index === 0 ? "selected" : ""}`;
    card.innerHTML = `
      ${gift.badge ? `<div class="gift-badge">${gift.badge}</div>` : ""}
      <div class="gift-sticker-box" style="box-shadow: 0 0 20px ${gift.glow_color || '#ff0054'}26;">
        <span class="gift-3d-emoji">${gift.emoji}</span>
      </div>
      <div class="gift-name">${gift.name}</div>
      <div class="gift-stars">${gift.stars_value} ⭐</div>
      <div class="gift-usd">$${gift.price_usd.toFixed(2)}</div>
    `;

    card.addEventListener("click", () => {
      haptic("medium");
      document.querySelectorAll(".gift-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      state.gifts.selectedGift = gift;
      const priceTag = document.getElementById("giftBtnPrice");
      if (priceTag) priceTag.textContent = `${gift.stars_value} ⭐ / $${gift.price_usd.toFixed(2)}`;
    });

    giftsGrid.appendChild(card);
  });

  state.gifts.selectedGift = data.packages[0];
}

// Setup Form Inputs and Actions
function setupInputs() {
  // For Myself Buttons
  document.getElementById("starsSelfBtn")?.addEventListener("click", () => {
    haptic("light");
    const targetInput = document.getElementById("starsTarget");
    if (targetInput) targetInput.value = getSelfRecipient();
  });

  document.getElementById("premSelfBtn")?.addEventListener("click", () => {
    haptic("light");
    const targetInput = document.getElementById("premTarget");
    if (targetInput) targetInput.value = getSelfRecipient();
  });

  document.getElementById("giftSelfBtn")?.addEventListener("click", () => {
    haptic("light");
    const targetInput = document.getElementById("giftTarget");
    if (targetInput) targetInput.value = getSelfRecipient();
  });

  // Custom stars input (Minimum 50 stars like Fragment)
  const customStarsInput = document.getElementById("customStarsInput");
  const customPriceTag = document.getElementById("customPriceTag");
  if (customStarsInput) {
    customStarsInput.addEventListener("input", (e) => {
      const val = parseInt(e.target.value, 10);
      if (val && val >= 50) {
        state.stars.customStars = val;
        state.stars.selectedPackage = null;
        document.querySelectorAll("#starsPackagesGrid .package-card").forEach((c) => c.classList.remove("selected"));
        const priceUsd = (val * 0.016).toFixed(2);
        if (customPriceTag) customPriceTag.textContent = `$${priceUsd}`;
        updateStarsButton();
      } else {
        state.stars.customStars = null;
        if (customPriceTag) customPriceTag.textContent = val ? "Min. 50 ⭐" : "$0.00";
      }
    });
  }

  // Gift character count
  const giftMsgInput = document.getElementById("giftMessage");
  const charCount = document.getElementById("giftCharCount");
  if (giftMsgInput && charCount) {
    giftMsgInput.addEventListener("input", (e) => {
      charCount.textContent = `${e.target.value.length}/128`;
    });
  }

  // Referral Copy & Share Buttons
  document.getElementById("copyRefBtn")?.addEventListener("click", () => {
    haptic("light");
    const link = document.getElementById("refLinkInput")?.value || state.referralLink;
    navigator.clipboard.writeText(link);
    showToast("Referral link copied!");
  });

  document.getElementById("shareRefTgBtn")?.addEventListener("click", () => {
    haptic("heavy");
    const link = document.getElementById("refLinkInput")?.value || state.referralLink;
    const text = encodeURIComponent("Join the Telegram Market for Stars, Premium, and Collectible Gifts!");
    const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(link)}&text=${text}`;
    if (tg?.openTelegramLink) {
      tg.openTelegramLink(shareUrl);
    } else {
      window.open(shareUrl, "_blank");
    }
  });

  // Order Stars to Account Button (Min 50 Stars Fragment Style)
  const btnOrderStars = document.getElementById("btnOrderStars");
  if (btnOrderStars) {
    btnOrderStars.addEventListener("click", () => {
      haptic("heavy");
      let target = document.getElementById("starsTarget")?.value.trim();
      if (!target) {
        target = getSelfRecipient();
        const targetInput = document.getElementById("starsTarget");
        if (targetInput) targetInput.value = target;
      }

      let starsCount = 50;
      let priceUsd = 0.99;
      let productName = "50 Telegram Stars";
      let productId = "stars_50";

      if (state.stars.customStars) {
        if (state.stars.customStars < 50) {
          showToast("Minimum order is 50 Stars (Fragment standard)!");
          return;
        }
        starsCount = state.stars.customStars;
        priceUsd = parseFloat((starsCount * 0.016).toFixed(2));
        productName = `${starsCount} Telegram Stars`;
        productId = `stars_custom_${starsCount}`;
      } else if (state.stars.selectedPackage) {
        const p = state.stars.selectedPackage;
        starsCount = p.stars_count;
        priceUsd = p.price_usd;
        productName = p.name;
        productId = p.id;
      }

      openCheckout({
        category: "stars",
        productId,
        productName,
        targetRecipient: target,
        priceStars: starsCount,
        priceUsd
      });
    });
  }

  // Order Telegram Premium Button (3m, 6m, 1y)
  const btnOrderPrem = document.getElementById("btnOrderPremium");
  if (btnOrderPrem) {
    btnOrderPrem.addEventListener("click", () => {
      haptic("heavy");
      let target = document.getElementById("premTarget")?.value.trim();
      if (!target) {
        target = getSelfRecipient();
        const targetInput = document.getElementById("premTarget");
        if (targetInput) targetInput.value = target;
      }

      const pkg = state.premium.selectedPackage || state.catalog.premium.packages[0];
      openCheckout({
        category: "premium",
        productId: pkg.id,
        productName: pkg.name,
        targetRecipient: target,
        priceStars: pkg.price_stars,
        priceUsd: pkg.price_usd,
        extraData: {
          duration_months: pkg.duration_months
        }
      });
    });
  }

  // Order Telegram Gift Button (15 to 100 Stars)
  const btnOrderGift = document.getElementById("btnOrderGift");
  if (btnOrderGift) {
    btnOrderGift.addEventListener("click", () => {
      haptic("heavy");
      let target = document.getElementById("giftTarget")?.value.trim();
      if (!target) {
        target = getSelfRecipient();
        const targetInput = document.getElementById("giftTarget");
        if (targetInput) targetInput.value = target;
      }

      const gift = state.gifts.selectedGift || state.catalog.gifts.packages[0];
      const msg = document.getElementById("giftMessage")?.value.trim() || "";
      const isAnon = document.getElementById("giftAnonymous")?.checked || false;

      openCheckout({
        category: "gifts",
        productId: gift.id,
        productName: `${gift.emoji} ${gift.name} Gift`,
        targetRecipient: target,
        priceStars: gift.stars_value,
        priceUsd: gift.price_usd,
        extraData: {
          gift_emoji: gift.emoji,
          message: msg,
          is_anonymous: isAnon
        }
      });
    });
  }
}

// ================= STARS TOP-UP MODAL =================
function setupTopupModal() {
  const modal = document.getElementById("topupModal");
  const openBtn = document.getElementById("openTopupBtn");
  const headerPill = document.getElementById("headerBalancePill");
  const closeBtn = document.getElementById("closeTopupBtn");
  const submitBtn = document.getElementById("btnSubmitTopup");

  if (!modal) return;

  const openModal = () => {
    haptic("medium");
    modal.classList.add("active");
  };

  const closeModal = () => {
    modal.classList.remove("active");
  };

  if (openBtn) openBtn.addEventListener("click", (e) => { e.stopPropagation(); openModal(); });
  if (headerPill) headerPill.addEventListener("click", openModal);
  if (closeBtn) closeBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  // Claim 5000 Demo Stars button
  const claimDemoBtn = document.getElementById("btnClaimDemoStars");
  if (claimDemoBtn) {
    claimDemoBtn.addEventListener("click", async () => {
      haptic("success");
      try {
        const res = await fetch(`/api/user/${state.user.id}/claim-demo`, { method: "POST" });
        const data = await res.json();
        if (data.ok) {
          state.user.balance_stars = data.balance_stars;
          updateUserProfile();
          showToast("🎉 +5,000 Demo Stars credited!");
          closeModal();
        }
      } catch (e) {
        state.user.balance_stars = (state.user.balance_stars || 0) + 5000;
        updateUserProfile();
        showToast("🎉 +5,000 Demo Stars credited!");
        closeModal();
      }
    });
  }

  // Custom Topup input
  const customInput = document.getElementById("customTopupInput");
  if (customInput) {
    customInput.addEventListener("input", (e) => {
      const val = parseInt(e.target.value, 10);
      if (val && val >= 10) {
        state.topup.selectedStars = val;
        document.querySelectorAll(".topup-pkg-card").forEach((c) => c.classList.remove("selected"));
        const btnText = document.getElementById("btnTopupText");
        if (btnText) btnText.textContent = `Top Up ${val} Stars`;
      }
    });
  }

  if (submitBtn) {
    submitBtn.addEventListener("click", async () => {
      haptic("heavy");
      const stars = state.topup.selectedStars;
      if (!stars || stars < 10) {
        showToast("Minimum top-up is 10 Stars");
        return;
      }

      const spinner = document.getElementById("btnTopupSpinner");
      const btnText = document.getElementById("btnTopupText");
      submitBtn.disabled = true;
      if (spinner) spinner.style.display = "inline-block";

      try {
        const res = await fetch("/api/balance/topup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: state.user.id, stars_count: stars })
        });
        const data = await res.json();
        if (!data.ok) throw new Error(data.detail || "Top-up failed");

        if (data.invoice_link) {
          if (tg?.openInvoice) {
            tg.openInvoice(data.invoice_link, async (status) => {
              if (status === "paid") {
                haptic("success");
                showToast(`🎉 +${stars} Stars deposited!`);
                closeModal();
                await fetchUserProfile();
              } else if (status === "cancelled") {
                showToast("Top-up was cancelled");
              }
            });
          } else {
            window.open(data.invoice_link, "_blank");
            showToast("Opening Telegram Stars invoice...");
            closeModal();
          }
        } else {
          showToast("Invoice link ready!");
        }
      } catch (err) {
        showToast(`Error: ${err.message}`);
      } finally {
        submitBtn.disabled = false;
        if (spinner) spinner.style.display = "none";
      }
    });
  }
}

function renderTopupPackages() {
  const grid = document.getElementById("topupGrid");
  const pkgs = state.catalog?.topup_packages || DEFAULT_CATALOG.topup_packages;
  if (!grid || !pkgs) return;

  grid.innerHTML = "";
  pkgs.forEach((pkg, index) => {
    const card = document.createElement("div");
    card.className = `topup-pkg-card ${index === 0 ? "selected" : ""}`;
    card.innerHTML = `
      ${pkg.badge ? `<div class="topup-badge">${pkg.badge}</div>` : ""}
      <div class="topup-stars">⭐ ${pkg.stars}</div>
      <div class="topup-usd">$${pkg.price_usd.toFixed(2)}</div>
    `;

    card.addEventListener("click", () => {
      haptic("medium");
      document.querySelectorAll(".topup-pkg-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      state.topup.selectedStars = pkg.stars;
      const customInput = document.getElementById("customTopupInput");
      if (customInput) customInput.value = "";
      const btnText = document.getElementById("btnTopupText");
      if (btnText) btnText.textContent = `Top Up ${pkg.stars} Stars ($${pkg.price_usd.toFixed(2)})`;
    });

    grid.appendChild(card);
  });

  state.topup.selectedStars = pkgs[0].stars;
  const btnText = document.getElementById("btnTopupText");
  if (btnText) btnText.textContent = `Top Up ${pkgs[0].stars} Stars ($${pkgs[0].price_usd.toFixed(2)})`;
}

// ================= CHECKOUT MODAL LOGIC =================
function setupCheckoutModal() {
  const modal = document.getElementById("checkoutModal");
  const closeBtn = document.getElementById("closeCheckoutBtn");

  if (closeBtn) closeBtn.addEventListener("click", closeCheckout);
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeCheckout();
    });
  }

  // Payment option toggle
  document.querySelectorAll(".payment-option").forEach((opt) => {
    opt.addEventListener("click", () => {
      haptic("light");
      document.querySelectorAll(".payment-option").forEach((o) => o.classList.remove("selected"));
      opt.classList.add("selected");
      const radio = opt.querySelector("input[type='radio']");
      if (radio) radio.checked = true;

      const method = opt.getAttribute("data-method");
      state.checkout.paymentMethod = method;
      updatePaymentDetailsView(method);
    });
  });

  // Copy buttons
  document.getElementById("copyAddressBtn")?.addEventListener("click", () => {
    haptic("light");
    const addr = document.getElementById("cryptoAddressInput")?.value || "";
    navigator.clipboard.writeText(addr);
    showToast("Address copied to clipboard!");
  });

  document.getElementById("copyCardBtn")?.addEventListener("click", () => {
    haptic("light");
    const card = document.getElementById("cardNumberText")?.textContent || "";
    navigator.clipboard.writeText(card.replace(/\s+/g, ""));
    showToast("Card number copied!");
  });

  // Submit Order Button
  document.getElementById("btnSubmitOrder")?.addEventListener("click", submitOrder);
}

function updatePaymentDetailsView(method) {
  const cryptoBox = document.getElementById("cryptoPaymentBox");
  const cardBox = document.getElementById("cardPaymentBox");

  if (cryptoBox) cryptoBox.style.display = "none";
  if (cardBox) cardBox.style.display = "none";

  if (method === "ton") {
    if (cryptoBox) cryptoBox.style.display = "block";
    const cfg = state.config?.crypto?.TON;
    const netLabel = document.getElementById("cryptoNetLabel");
    if (netLabel) netLabel.textContent = "TON Wallet Address:";
    const addrInput = document.getElementById("cryptoAddressInput");
    if (addrInput) addrInput.value = cfg?.address || "UQDC7q9w2Z0r8GvKxY9_TON_WALLET";
    const qrImg = document.getElementById("cryptoQrImg");
    if (qrImg) qrImg.src = (cfg?.qr_code_url || "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=") + (cfg?.address || "");
  } else if (method === "usdt") {
    if (cryptoBox) cryptoBox.style.display = "block";
    const cfg = state.config?.crypto?.USDT;
    const netLabel = document.getElementById("cryptoNetLabel");
    if (netLabel) netLabel.textContent = "USDT Address (TRC-20 / TON):";
    const addrInput = document.getElementById("cryptoAddressInput");
    if (addrInput) addrInput.value = cfg?.address || "TYx123456789_USDT_WALLET";
    const qrImg = document.getElementById("cryptoQrImg");
    if (qrImg) qrImg.src = (cfg?.qr_code_url || "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=") + (cfg?.address || "");
  } else if (method === "card") {
    if (cardBox) cardBox.style.display = "block";
    const cfg = state.config?.card;
    const cardNum = document.getElementById("cardNumberText");
    if (cardNum) cardNum.textContent = cfg?.card_number || "8600 0000 0000 0000";
    const bankInfo = document.getElementById("cardBankInfo");
    if (bankInfo) bankInfo.textContent = `${cfg?.bank_name || 'Bank Card'} (${cfg?.holder_name || 'Store'})`;
  }
}

function openCheckout(item) {
  state.checkout.item = item;
  
  // Balance description
  const bal = state.user.balance_stars || 0;
  const isSufficient = bal >= item.priceStars;
  const balDesc = document.getElementById("balanceDesc");
  if (balDesc) {
    balDesc.textContent = `Available balance: ${bal} ⭐ ${!isSufficient ? `(Need +${item.priceStars - bal} ⭐)` : '✅ Sufficient'}`;
  }
  
  const balOption = document.querySelector(".payment-option[data-method='balance']");
  if (item.category === "stars") {
    if (balOption) balOption.style.display = "none";
    state.checkout.paymentMethod = "ton"; // Default to TON for Fragment style Stars
  } else {
    if (balOption) balOption.style.display = "flex";
    state.checkout.paymentMethod = isSufficient ? "balance" : "stars";
  }

  const sumProduct = document.getElementById("summaryProduct");
  if (sumProduct) sumProduct.textContent = item.productName;
  const sumTarget = document.getElementById("summaryTarget");
  if (sumTarget) sumTarget.textContent = `Target Account: ${item.targetRecipient}`;
  
  let extraText = "";
  if (item.category === "gifts" && item.extraData?.is_anonymous) {
    extraText = "🕵️ Anonymous Profile Gift";
  } else if (item.category === "premium" && item.extraData?.duration_months) {
    extraText = `⏱️ Duration: ${item.extraData.duration_months} Months`;
  }
  const sumExtra = document.getElementById("summaryExtra");
  if (sumExtra) sumExtra.textContent = extraText;
  const sumPrice = document.getElementById("summaryPrice");
  if (sumPrice) sumPrice.textContent = `${item.priceStars} ⭐ / $${item.priceUsd.toFixed(2)}`;

  // Update selected payment radio
  document.querySelectorAll(".payment-option").forEach((o) => {
    const isSelected = o.getAttribute("data-method") === state.checkout.paymentMethod;
    o.classList.toggle("selected", isSelected);
    const radio = o.querySelector("input");
    if (radio) radio.checked = isSelected;
  });
  updatePaymentDetailsView(state.checkout.paymentMethod);

  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.add("active");

  if (tg?.BackButton) {
    tg.BackButton.show();
    tg.BackButton.onClick(closeCheckout);
  }
}

function closeCheckout() {
  const modal = document.getElementById("checkoutModal");
  if (modal) modal.classList.remove("active");
  if (tg?.BackButton && state.activeTab !== "admin") {
    tg.BackButton.hide();
  }
}

async function submitOrder() {
  const item = state.checkout.item;
  if (!item) return;

  // Check if balance is selected and sufficient
  if (state.checkout.paymentMethod === "balance") {
    const bal = state.user.balance_stars || 0;
    if (bal < item.priceStars) {
      haptic("error");
      showToast(`Insufficient Stars balance! Please top up your balance.`);
      closeCheckout();
      const topupM = document.getElementById("topupModal");
      if (topupM) topupM.classList.add("active");
      return;
    }
  }

  const btn = document.getElementById("btnSubmitOrder");
  const spinner = document.getElementById("btnSpinner");
  const btnText = document.getElementById("btnSubmitText");

  if (btn) btn.disabled = true;
  if (spinner) spinner.style.display = "inline-block";
  if (btnText) btnText.textContent = "Processing...";

  const payload = {
    user_id: state.user.id,
    user_name: state.user.username ? `@${state.user.username}` : (state.user.first_name || "User"),
    category: item.category,
    product_id: item.productId,
    product_name: item.productName,
    quantity: 1,
    price_usd: item.priceUsd,
    price_stars: item.priceStars,
    target_recipient: item.targetRecipient,
    extra_data: item.extraData || {},
    payment_method: state.checkout.paymentMethod
  };

  try {
    const res = await fetch("/api/orders/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!data.ok) throw new Error(data.detail || "Order failed");

    const order = data.order;
    const invoiceLink = data.invoice_link;

    // Handle Payment Method
    if (state.checkout.paymentMethod === "balance") {
      haptic("success");
      state.user.balance_stars = data.new_balance;
      updateUserProfile();
      showToast(`🎉 Order #${order.order_uuid} paid instantly from Stars balance!`);
      closeCheckout();
      switchTab("orders");
      loadUserOrders();
    } else if (state.checkout.paymentMethod === "stars" && invoiceLink) {
      if (tg?.openInvoice) {
        tg.openInvoice(invoiceLink, (status) => {
          if (status === "paid") {
            haptic("success");
            showToast("🎉 Telegram Stars payment successful!");
            closeCheckout();
            switchTab("orders");
            loadUserOrders();
          } else if (status === "cancelled") {
            showToast("Payment was cancelled");
          }
        });
      } else {
        window.open(invoiceLink, "_blank");
        showToast("Opening Telegram Stars invoice...");
        closeCheckout();
        switchTab("orders");
        loadUserOrders();
      }
    } else {
      haptic("success");
      showToast(`Order #${order.order_uuid} placed! Delivery to ${item.targetRecipient}.`);
      closeCheckout();
      switchTab("orders");
      loadUserOrders();
    }
  } catch (err) {
    haptic("error");
    showToast(`Error: ${err.message}`);
  } finally {
    if (btn) btn.disabled = false;
    if (spinner) spinner.style.display = "none";
    if (btnText) btnText.textContent = "Proceed to Pay";
  }
}

// ================= TAB 5: MY ORDERS =================
async function loadUserOrders() {
  const container = document.getElementById("ordersList");
  const badge = document.getElementById("ordersBadge");
  if (!container) return;

  try {
    const res = await fetch(`/api/orders/user/${state.user.id}`);
    const data = await res.json();

    if (data.ok && data.orders && data.orders.length > 0) {
      if (badge) {
        badge.textContent = data.orders.length;
        badge.style.display = "inline-block";
      }

      container.innerHTML = "";
      data.orders.forEach((o) => {
        const item = document.createElement("div");
        item.className = "order-item-card";

        const formattedDate = new Date(o.created_at).toLocaleString();
        item.innerHTML = `
          <div class="order-item-top">
            <span class="order-id">#${o.order_uuid}</span>
            <span class="order-status-badge ${o.status}">${o.status}</span>
          </div>
          <div class="order-item-title">${o.product_name}</div>
          <div class="order-item-target">🎯 ${o.target_recipient}</div>
          <div class="order-item-bottom">
            <span class="order-date">${formattedDate}</span>
            <span class="order-price">${o.price_stars} ⭐ ($${o.price_usd})</span>
          </div>
        `;
        container.appendChild(item);
      });
    } else {
      if (badge) badge.style.display = "none";
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">🛒</div>
          <h3>No Orders Yet</h3>
          <p>Your purchased Telegram Stars, Premium, and Gifts will appear here.</p>
        </div>
      `;
    }
  } catch (err) {
    console.error("Failed to load orders:", err);
  }
}

// ================= ADMIN DASHBOARD =================
async function loadAdminDashboard() {
  const statOrders = document.getElementById("statOrders");
  const statRevenue = document.getElementById("statRevenue");
  const statPending = document.getElementById("statPending");
  const list = document.getElementById("adminOrdersList");
  if (!list) return;

  try {
    const res = await fetch("/api/admin/orders");
    const data = await res.json();

    if (data.ok) {
      if (statOrders) statOrders.textContent = data.stats.total_orders;
      if (statRevenue) statRevenue.textContent = `$${data.stats.total_usd}`;
      if (statPending) statPending.textContent = data.stats.pending_count;

      list.innerHTML = "";
      if (data.orders.length === 0) {
        list.innerHTML = `<div class="empty-state">No orders placed yet.</div>`;
        return;
      }

      data.orders.forEach((o) => {
        const row = document.createElement("div");
        row.className = "admin-order-row";
        row.innerHTML = `
          <div class="admin-order-meta">
            <strong>#${o.order_uuid} - ${o.product_name}</strong>
            <span>Customer: ${o.user_name} | Target: ${o.target_recipient}</span>
            <span>Price: ${o.price_stars} ⭐ ($${o.price_usd}) | Status: <b>${o.status.toUpperCase()}</b></span>
          </div>
          <div class="admin-actions">
            ${o.status !== "completed" ? `<button class="btn-admin-done" data-id="${o.order_uuid}">Done ✅</button>` : ""}
            ${o.status !== "cancelled" ? `<button class="btn-admin-cancel" data-id="${o.order_uuid}">Cancel ❌</button>` : ""}
          </div>
        `;

        const doneBtn = row.querySelector(".btn-admin-done");
        if (doneBtn) {
          doneBtn.addEventListener("click", () => updateAdminStatus(o.order_uuid, "completed"));
        }
        const cancelBtn = row.querySelector(".btn-admin-cancel");
        if (cancelBtn) {
          cancelBtn.addEventListener("click", () => updateAdminStatus(o.order_uuid, "cancelled"));
        }

        list.appendChild(row);
      });
    }
  } catch (err) {
    console.error("Failed to load admin dashboard:", err);
  }
}

async function updateAdminStatus(orderId, newStatus) {
  haptic("medium");
  try {
    const res = await fetch(`/api/admin/orders/${orderId}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus })
    });
    const data = await res.json();
    if (data.ok) {
      showToast(`Order #${orderId} marked as ${newStatus}!`);
      loadAdminDashboard();
    }
  } catch (err) {
    showToast(`Error: ${err.message}`);
  }
}
