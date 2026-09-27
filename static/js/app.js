// Telegram Web App Market Application Logic

const tg = window.Telegram?.WebApp || null;

// Application State
const state = {
  user: {
    id: 12345678,
    first_name: "Demo User",
    username: "telegram_user",
    balance_stars: 0,
    referral_count: 0,
    referral_earnings: 0,
    language_code: "en"
  },
  activeTab: "reactions",
  catalog: null,
  config: null,
  isAdmin: false,
  referralLink: "",
  
  // Selection states
  reactions: {
    selectedPackage: null,
    selectedEmoji: "⭐",
    customStars: null,
    targetLink: ""
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
    selectedStars: 100
  },
  
  // Checkout
  checkout: {
    item: null,
    paymentMethod: "balance"
  }
};

// Multilingual Dictionary
const i18n = {
  en: {
    tab_reactions: "Reactions",
    tab_premium: "Premium",
    tab_gifts: "3D Gifts",
    tab_referrals: "Referrals",
    tab_orders: "Orders",
    label_post_link: "Telegram Post / Channel Link",
    choose_emoji: "Choose Reaction Sticker",
    select_package: "Select Stars Package",
    label_recipient: "Recipient Telegram Username",
    select_duration: "Select Duration",
    label_gift_recipient: "Recipient Username",
    choose_gift: "Choose a 3D Collectible Gift",
    btn_order_reactions: "Order Paid Reactions",
    btn_order_premium: "Gift Telegram Premium",
    btn_order_gift: "Send Telegram Gift",
    proceed_to_pay: "Proceed to Pay",
    link_required: "Please enter a valid Telegram post link!",
    username_required: "Please enter a recipient Telegram username!"
  },
  ru: {
    tab_reactions: "Реакции",
    tab_premium: "Премиум",
    tab_gifts: "3D Подарки",
    tab_referrals: "Рефералы",
    tab_orders: "Заказы",
    label_post_link: "Ссылка на пост / канал",
    choose_emoji: "Выберите стикер реакции",
    select_package: "Выберите пакет Звёзд",
    label_recipient: "Юзернейм получателя",
    select_duration: "Срок подписки",
    label_gift_recipient: "Юзернейм получателя",
    choose_gift: "Выберите 3D подарок",
    btn_order_reactions: "Заказать реакции",
    btn_order_premium: "Подарить Premium",
    btn_order_gift: "Отправить подарок",
    proceed_to_pay: "Оплатить заказ",
    link_required: "Пожалуйста, введите ссылку на пост Telegram!",
    username_required: "Пожалуйста, введите юзернейм получателя!"
  },
  uz: {
    tab_reactions: "Reaksiyalar",
    tab_premium: "Premium",
    tab_gifts: "3D Sovg'alar",
    tab_referrals: "Referallar",
    tab_orders: "Buyurtmalar",
    label_post_link: "Telegram post / kanal havolasi",
    choose_emoji: "Reaksiya stikerini tanlang",
    select_package: "Yulduzlar paketini tanlang",
    label_recipient: "Qabul qiluvchi username",
    select_duration: "Obuna muddatini tanlang",
    label_gift_recipient: "Qabul qiluvchi username",
    choose_gift: "3D sovg'ani tanlang",
    btn_order_reactions: "Reaksiyalarni buyurtma qilish",
    btn_order_premium: "Premium sovg'a qilish",
    btn_order_gift: "Sovg'a yuborish",
    proceed_to_pay: "To'lovni amalga oshirish",
    link_required: "Iltimos, Telegram post havolasini kiriting!",
    username_required: "Iltimos, qabul qiluvchi usernameni kiriting!"
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
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 2800);
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

  // Load app data & user profile
  await Promise.all([
    fetchAppData(),
    fetchUserProfile()
  ]);

  renderReactionsTab();
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
    userNameEl.textContent = state.user.first_name || "Telegram User";
    userHandleEl.textContent = state.user.username ? `@${state.user.username}` : `ID: ${state.user.id}`;
    avatarEl.textContent = (state.user.first_name || "T")[0].toUpperCase();
    balanceEl.textContent = state.user.balance_stars || 0;
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
  adminToggleBtn.addEventListener("click", () => {
    haptic("medium");
    switchTab("admin");
    loadAdminDashboard();
  });

  const closeAdminBtn = document.getElementById("closeAdminBtn");
  closeAdminBtn.addEventListener("click", () => {
    switchTab("reactions");
  });

  const refreshOrdersBtn = document.getElementById("refreshOrdersBtn");
  refreshOrdersBtn.addEventListener("click", () => {
    haptic("light");
    loadUserOrders();
  });
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
      tg.BackButton.onClick(() => switchTab("reactions"));
    } else {
      tg.BackButton.hide();
    }
  }
}

// Language Switcher
function setupLanguageSwitcher() {
  const langSelect = document.getElementById("langSelect");
  langSelect.addEventListener("change", (e) => {
    currentLang = e.target.value;
    haptic("light");
    applyTranslations();
  });
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
      fetch("/api/catalog").then((r) => r.json()),
      fetch("/api/config").then((r) => r.json())
    ]);

    if (catRes.ok) {
      state.catalog = catRes.catalog;
    }
    if (cfgRes) {
      state.config = cfgRes;
      if (cfgRes.admin_ids && cfgRes.admin_ids.includes(state.user.id)) {
        state.isAdmin = true;
        document.getElementById("adminToggleBtn").style.display = "block";
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

      // Update Referrals Tab elements
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

// ================= TAB 1: PAID REACTIONS =================
function renderReactionsTab() {
  if (!state.catalog?.reactions) return;

  const data = state.catalog.reactions;

  // Render Modern Reaction Stickers
  const emojiGrid = document.getElementById("emojiGrid");
  emojiGrid.innerHTML = "";
  data.emoji_options.forEach((item, index) => {
    const el = document.createElement("div");
    el.className = `sticker-item ${index === 0 ? "selected" : ""}`;
    el.textContent = item.emoji;
    el.title = item.name;
    el.addEventListener("click", () => {
      haptic("light");
      document.querySelectorAll(".sticker-item").forEach((e) => e.classList.remove("selected"));
      el.classList.add("selected");
      state.reactions.selectedEmoji = item.emoji;
      document.getElementById("selectedEmojiPreview").textContent = `${item.emoji} ${item.name}`;
    });
    emojiGrid.appendChild(el);
  });

  // Render Packages
  const pkgGrid = document.getElementById("reactionsPackagesGrid");
  pkgGrid.innerHTML = "";
  data.packages.forEach((pkg, index) => {
    const card = document.createElement("div");
    card.className = `package-card ${index === 0 ? "selected" : ""}`;
    card.innerHTML = `
      ${pkg.badge ? `<div class="package-badge">${pkg.badge}</div>` : ""}
      <div class="package-stars">⭐ ${pkg.stars_count}</div>
      <div class="package-price">$${pkg.price_usd.toFixed(2)}</div>
      <div class="package-time">⚡ ${pkg.delivery_time}</div>
    `;

    card.addEventListener("click", () => {
      haptic("medium");
      document.querySelectorAll(".package-card").forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      state.reactions.selectedPackage = pkg;
      state.reactions.customStars = null;
      document.getElementById("customStarsInput").value = "";
      updateReactionButton();
    });

    pkgGrid.appendChild(card);
  });

  state.reactions.selectedPackage = data.packages[0];
  updateReactionButton();
}

function updateReactionButton() {
  const priceTag = document.getElementById("reactBtnPrice");
  if (state.reactions.customStars) {
    const priceUsd = (state.reactions.customStars * 0.016).toFixed(2);
    priceTag.textContent = `${state.reactions.customStars} ⭐ / $${priceUsd}`;
  } else if (state.reactions.selectedPackage) {
    const pkg = state.reactions.selectedPackage;
    priceTag.textContent = `${pkg.stars_count} ⭐ / $${pkg.price_usd.toFixed(2)}`;
  }
}

// ================= TAB 2: TELEGRAM PREMIUM =================
function renderPremiumTab() {
  if (!state.catalog?.premium) return;

  const data = state.catalog.premium;
  const pkgGrid = document.getElementById("premiumPackagesGrid");
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
      document.getElementById("premBtnPrice").textContent = `$${pkg.price_usd.toFixed(2)}`;
    });

    pkgGrid.appendChild(card);
  });

  state.premium.selectedPackage = data.packages[1];

  const perksGrid = document.getElementById("perksGrid");
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

// ================= TAB 3: MODERN 3D GIFTS =================
function renderGiftsTab() {
  if (!state.catalog?.gifts) return;

  const data = state.catalog.gifts;
  const giftsGrid = document.getElementById("giftsGrid");
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
      document.getElementById("giftBtnPrice").textContent = `${gift.stars_value} ⭐ / $${gift.price_usd.toFixed(2)}`;
    });

    giftsGrid.appendChild(card);
  });

  state.gifts.selectedGift = data.packages[0];
}

// Setup Form Inputs and Actions
function setupInputs() {
  // Post Link Paste
  const pasteBtn = document.getElementById("reactPasteBtn");
  pasteBtn.addEventListener("click", async () => {
    haptic("light");
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const text = await navigator.clipboard.readText();
        if (text) document.getElementById("reactTarget").value = text;
      }
    } catch (e) {
      showToast("Please type or paste the link manually");
    }
  });

  // Custom stars input
  const customStarsInput = document.getElementById("customStarsInput");
  const customPriceTag = document.getElementById("customPriceTag");
  customStarsInput.addEventListener("input", (e) => {
    const val = parseInt(e.target.value, 10);
    if (val && val >= 50) {
      state.reactions.customStars = val;
      state.reactions.selectedPackage = null;
      document.querySelectorAll(".package-card").forEach((c) => c.classList.remove("selected"));
      const priceUsd = (val * 0.016).toFixed(2);
      customPriceTag.textContent = `$${priceUsd}`;
      updateReactionButton();
    } else {
      state.reactions.customStars = null;
      customPriceTag.textContent = "$0.00";
    }
  });

  // For Myself Buttons
  document.getElementById("premSelfBtn").addEventListener("click", () => {
    haptic("light");
    const uname = state.user.username || state.user.first_name;
    document.getElementById("premTarget").value = uname ? `@${uname.replace('@','')}` : "";
  });

  document.getElementById("giftSelfBtn").addEventListener("click", () => {
    haptic("light");
    const uname = state.user.username || state.user.first_name;
    document.getElementById("giftTarget").value = uname ? `@${uname.replace('@','')}` : "";
  });

  // Gift character count
  const giftMsgInput = document.getElementById("giftMessage");
  const charCount = document.getElementById("giftCharCount");
  giftMsgInput.addEventListener("input", (e) => {
    charCount.textContent = `${e.target.value.length}/128`;
  });

  // Referral Copy & Share Buttons
  document.getElementById("copyRefBtn").addEventListener("click", () => {
    haptic("light");
    const link = document.getElementById("refLinkInput").value;
    navigator.clipboard.writeText(link);
    showToast("Referral link copied!");
  });

  document.getElementById("shareRefTgBtn").addEventListener("click", () => {
    haptic("heavy");
    const link = document.getElementById("refLinkInput").value;
    const text = encodeURIComponent("Join the Telegram Market to get Paid Reactions, Telegram Premium, and Collectible 3D Gifts!");
    const shareUrl = `https://t.me/share/url?url=${encodeURIComponent(link)}&text=${text}`;
    if (tg?.openTelegramLink) {
      tg.openTelegramLink(shareUrl);
    } else {
      window.open(shareUrl, "_blank");
    }
  });

  // Order Buttons
  document.getElementById("btnOrderReactions").addEventListener("click", () => {
    haptic("heavy");
    const target = document.getElementById("reactTarget").value.trim();
    if (!target) {
      showToast(i18n[currentLang]?.link_required || "Please enter a post link!");
      document.getElementById("reactTarget").focus();
      return;
    }

    let starsCount = 50;
    let priceUsd = 0.99;
    let productName = "50 Paid Stars Reactions";
    let productId = "react_50";

    if (state.reactions.customStars) {
      starsCount = state.reactions.customStars;
      priceUsd = parseFloat((starsCount * 0.016).toFixed(2));
      productName = `${starsCount} Paid Stars Reactions`;
      productId = `react_custom_${starsCount}`;
    } else if (state.reactions.selectedPackage) {
      const p = state.reactions.selectedPackage;
      starsCount = p.stars_count;
      priceUsd = p.price_usd;
      productName = p.name;
      productId = p.id;
    }

    openCheckout({
      category: "reactions",
      productId,
      productName,
      targetRecipient: target,
      priceStars: starsCount,
      priceUsd,
      extraData: {
        emoji: state.reactions.selectedEmoji
      }
    });
  });

  document.getElementById("btnOrderPremium").addEventListener("click", () => {
    haptic("heavy");
    const target = document.getElementById("premTarget").value.trim();
    if (!target) {
      showToast(i18n[currentLang]?.username_required || "Please enter recipient username!");
      document.getElementById("premTarget").focus();
      return;
    }

    const pkg = state.premium.selectedPackage;
    openCheckout({
      category: "premium",
      productId: pkg.id,
      productName: pkg.name,
      targetRecipient: target.startsWith("@") ? target : `@${target}`,
      priceStars: pkg.price_stars,
      priceUsd: pkg.price_usd,
      extraData: {
        duration_months: pkg.duration_months
      }
    });
  });

  document.getElementById("btnOrderGift").addEventListener("click", () => {
    haptic("heavy");
    const target = document.getElementById("giftTarget").value.trim();
    if (!target) {
      showToast(i18n[currentLang]?.username_required || "Please enter recipient username!");
      document.getElementById("giftTarget").focus();
      return;
    }

    const gift = state.gifts.selectedGift;
    const msg = document.getElementById("giftMessage").value.trim();
    const isAnon = document.getElementById("giftAnonymous").checked;

    openCheckout({
      category: "gifts",
      productId: gift.id,
      productName: `${gift.emoji} ${gift.name} 3D Gift`,
      targetRecipient: target.startsWith("@") ? target : `@${target}`,
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

// ================= STARS TOP-UP MODAL =================
function setupTopupModal() {
  const modal = document.getElementById("topupModal");
  const openBtn = document.getElementById("openTopupBtn");
  const headerPill = document.getElementById("headerBalancePill");
  const closeBtn = document.getElementById("closeTopupBtn");
  const submitBtn = document.getElementById("btnSubmitTopup");

  const openModal = () => {
    haptic("medium");
    modal.classList.add("active");
  };

  const closeModal = () => {
    modal.classList.remove("active");
  };

  openBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    openModal();
  });
  headerPill.addEventListener("click", openModal);
  closeBtn.addEventListener("click", closeModal);
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
          showToast("🎉 +5,000 Demo Stars added to balance!");
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
  customInput.addEventListener("input", (e) => {
    const val = parseInt(e.target.value, 10);
    if (val && val >= 10) {
      state.topup.selectedStars = val;
      document.querySelectorAll(".topup-pkg-card").forEach((c) => c.classList.remove("selected"));
      document.getElementById("btnTopupText").textContent = `Top Up ${val} Stars`;
    }
  });

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
    spinner.style.display = "inline-block";

    try {
      const res = await fetch("/api/balance/topup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: state.user.id, stars_count: stars })
      });
      const data = await res.json();
      if (!data.ok) throw new Error(data.detail || "Top-up failed");

      if (data.invoice_link && tg?.openInvoice) {
        tg.openInvoice(data.invoice_link, async (status) => {
          if (status === "paid") {
            haptic("success");
            showToast(`🎉 +${stars} Stars deposited to your balance!`);
            closeModal();
            await fetchUserProfile();
          } else if (status === "cancelled") {
            showToast("Top-up was cancelled");
          }
        });
      } else {
        showToast("Invoice link ready!");
      }
    } catch (err) {
      showToast(`Error: ${err.message}`);
    } finally {
      submitBtn.disabled = false;
      spinner.style.display = "none";
    }
  });
}

function renderTopupPackages() {
  const grid = document.getElementById("topupGrid");
  if (!grid || !state.catalog?.topup_packages) return;

  grid.innerHTML = "";
  state.catalog.topup_packages.forEach((pkg, index) => {
    const card = document.createElement("div");
    card.className = `topup-pkg-card ${index === 1 ? "selected" : ""}`;
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
      document.getElementById("customTopupInput").value = "";
      document.getElementById("btnTopupText").textContent = `Top Up ${pkg.stars} Stars ($${pkg.price_usd.toFixed(2)})`;
    });

    grid.appendChild(card);
  });

  state.topup.selectedStars = state.catalog.topup_packages[1].stars;
  document.getElementById("btnTopupText").textContent = `Top Up 100 Stars ($1.89)`;
}

// ================= CHECKOUT MODAL LOGIC =================
function setupCheckoutModal() {
  const modal = document.getElementById("checkoutModal");
  const closeBtn = document.getElementById("closeCheckoutBtn");

  closeBtn.addEventListener("click", closeCheckout);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeCheckout();
  });

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
  document.getElementById("copyAddressBtn").addEventListener("click", () => {
    haptic("light");
    const addr = document.getElementById("cryptoAddressInput").value;
    navigator.clipboard.writeText(addr);
    showToast("Address copied to clipboard!");
  });

  document.getElementById("copyCardBtn").addEventListener("click", () => {
    haptic("light");
    const card = document.getElementById("cardNumberText").textContent;
    navigator.clipboard.writeText(card.replace(/\s+/g, ""));
    showToast("Card number copied!");
  });

  // Submit Order Button
  document.getElementById("btnSubmitOrder").addEventListener("click", submitOrder);
}

function updatePaymentDetailsView(method) {
  const cryptoBox = document.getElementById("cryptoPaymentBox");
  const cardBox = document.getElementById("cardPaymentBox");

  cryptoBox.style.display = "none";
  cardBox.style.display = "none";

  if (method === "ton") {
    cryptoBox.style.display = "block";
    const cfg = state.config?.crypto?.TON;
    document.getElementById("cryptoNetLabel").textContent = "TON Wallet Address:";
    document.getElementById("cryptoAddressInput").value = cfg?.address || "UQ_TON_WALLET_ADDRESS";
    document.getElementById("cryptoQrImg").src = (cfg?.qr_code_url || "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=") + (cfg?.address || "");
  } else if (method === "usdt") {
    cryptoBox.style.display = "block";
    const cfg = state.config?.crypto?.USDT;
    document.getElementById("cryptoNetLabel").textContent = "USDT Address (TRC-20):";
    document.getElementById("cryptoAddressInput").value = cfg?.address || "TYx_USDT_ADDRESS";
    document.getElementById("cryptoQrImg").src = (cfg?.qr_code_url || "https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=") + (cfg?.address || "");
  } else if (method === "card") {
    cardBox.style.display = "block";
    const cfg = state.config?.card;
    document.getElementById("cardNumberText").textContent = cfg?.card_number || "8600 0000 0000 0000";
    document.getElementById("cardBankInfo").textContent = `${cfg?.bank_name || 'Bank Transfer'} (${cfg?.holder_name || 'Store'})`;
  }
}

function openCheckout(item) {
  state.checkout.item = item;
  
  // Update balance description
  const bal = state.user.balance_stars || 0;
  const isSufficient = bal >= item.priceStars;
  const balDesc = document.getElementById("balanceDesc");
  balDesc.textContent = `Available balance: ${bal} ⭐ ${!isSufficient ? `(Need +${item.priceStars - bal} ⭐)` : '✅ Sufficient'}`;
  
  // Default to balance if sufficient, else fallback to stars
  state.checkout.paymentMethod = isSufficient ? "balance" : "stars";

  document.getElementById("summaryProduct").textContent = item.productName;
  document.getElementById("summaryTarget").textContent = `Target: ${item.targetRecipient}`;
  
  let extraText = "";
  if (item.category === "reactions" && item.extraData?.emoji) {
    extraText = `Reaction Sticker: ${item.extraData.emoji}`;
  } else if (item.category === "gifts") {
    extraText = item.extraData?.is_anonymous ? "🕵️ Anonymous Gift" : "";
  }
  document.getElementById("summaryExtra").textContent = extraText;
  document.getElementById("summaryPrice").textContent = `${item.priceStars} ⭐ / $${item.priceUsd.toFixed(2)}`;

  // Update selected radio
  document.querySelectorAll(".payment-option").forEach((o) => {
    const isSelected = o.getAttribute("data-method") === state.checkout.paymentMethod;
    o.classList.toggle("selected", isSelected);
    o.querySelector("input").checked = isSelected;
  });
  updatePaymentDetailsView(state.checkout.paymentMethod);

  document.getElementById("checkoutModal").classList.add("active");

  if (tg?.BackButton) {
    tg.BackButton.show();
    tg.BackButton.onClick(closeCheckout);
  }
}

function closeCheckout() {
  document.getElementById("checkoutModal").classList.remove("active");
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
      document.getElementById("topupModal").classList.add("active");
      return;
    }
  }

  const btn = document.getElementById("btnSubmitOrder");
  const spinner = document.getElementById("btnSpinner");
  const btnText = document.getElementById("btnSubmitText");

  btn.disabled = true;
  spinner.style.display = "inline-block";
  btnText.textContent = "Processing...";

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
    } else if (state.checkout.paymentMethod === "stars" && invoiceLink && tg?.openInvoice) {
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
      haptic("success");
      showToast(`Order #${order.order_uuid} placed! We will process it shortly.`);
      closeCheckout();
      switchTab("orders");
      loadUserOrders();
    }
  } catch (err) {
    haptic("error");
    showToast(`Error: ${err.message}`);
  } finally {
    btn.disabled = false;
    spinner.style.display = "none";
    btnText.textContent = "Proceed to Pay";
  }
}

// ================= TAB 5: MY ORDERS =================
async function loadUserOrders() {
  const container = document.getElementById("ordersList");
  const badge = document.getElementById("ordersBadge");

  try {
    const res = await fetch(`/api/orders/user/${state.user.id}`);
    const data = await res.json();

    if (data.ok && data.orders && data.orders.length > 0) {
      badge.textContent = data.orders.length;
      badge.style.display = "inline-block";

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
      badge.style.display = "none";
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">🛒</div>
          <h3>No Orders Yet</h3>
          <p>Your purchased Paid Reactions, Premium, and Gifts will appear here.</p>
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

  try {
    const res = await fetch("/api/admin/orders");
    const data = await res.json();

    if (data.ok) {
      statOrders.textContent = data.stats.total_orders;
      statRevenue.textContent = `$${data.stats.total_usd}`;
      statPending.textContent = data.stats.pending_count;

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
