/* ═══════════════════════════════════════════════════════════════════════════
   CS Triplet Eatery — Storefront Application Logic
   ═══════════════════════════════════════════════════════════════════════════ */

// ─── State ───────────────────────────────────────────────────────────────────
let menuData = {};          // { category_key: [items] }
let categoryLabels = {};    // { category_key: 'Display Name' }
let cart = [];              // [{ menuItemId, name, price, quantity }]
let activeCategory = 'starters';

// ─── Category Emoji Map ──────────────────────────────────────────────────────
const categoryEmoji = {
  starters:  '🍢',
  fast_food: '🍔',
  non_veg:   '🍗',
  regular:   '🍛',
  breads:    '🫓',
  soups:     '🍲',
  beverages: '🥤',
  desserts:  '🍮',
};

// ─── Section Navigation ─────────────────────────────────────────────────────
const overlaySections = ['cart-section', 'checkout-section', 'receipt-section'];

function showSection(sectionId) {
  if (overlaySections.includes(sectionId)) {
    const section = document.getElementById(sectionId);
    section.classList.add('active');
    section.style.animation = 'none';
    section.offsetHeight;
    section.style.animation = '';
    document.body.style.overflow = 'hidden';
  }

  window.scrollTo({ top: 0, behavior: 'instant' });

  if (sectionId === 'cart-section') renderCart();
  if (sectionId === 'checkout-section') renderCheckout();
  if (sectionId === 'menu-section') {
    document.getElementById('menu-section').scrollIntoView({ behavior: 'smooth' });
  }
}

function closeOverlay() {
  overlaySections.forEach((id) => document.getElementById(id).classList.remove('active'));
  document.body.style.overflow = '';
}

// ─── Fetch Menu ──────────────────────────────────────────────────────────────
async function fetchMenu() {
  try {
    const res = await fetch('/api/menu');
    const data = await res.json();
    menuData = data.menu;
    categoryLabels = data.labels;

    // Set first category as default
    const categories = Object.keys(menuData);
    if (categories.length > 0) activeCategory = categories[0];

    buildCategoryTabs();
    renderMenu();
  } catch (err) {
    console.error('Failed to fetch menu:', err);
    document.getElementById('menu-grid').innerHTML =
      '<p style="color:var(--text-muted);text-align:center;grid-column:1/-1;padding:60px 0;">Could not load menu. Make sure the server is running and the database is set up.</p>';
  }
}

// ─── Build Category Tabs Dynamically ────────────────────────────────────────
function buildCategoryTabs() {
  const container = document.getElementById('menu-tabs');
  container.innerHTML = Object.keys(menuData)
    .map((cat, idx) => {
      const label = categoryLabels[cat] || cat;
      const emoji = categoryEmoji[cat] || '🍽️';
      const isActive = cat === activeCategory ? 'active' : '';
      return `<button class="menu-tab ${isActive}" data-category="${cat}" onclick="switchCategory('${cat}', this)">${emoji} ${label}</button>`;
    })
    .join('');
}

// ─── Image Mapping ───────────────────────────────────────────────────────────
const itemImages = {
  // ── Fast Food ──
  'Pasta':               'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=500&q=80',
  'Pizza':               'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&q=80',
  'Burger':              'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&q=80',
  'Fried Rice':          'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=500&q=80',
  'Manchurian':          'https://images.unsplash.com/photo-1534422298391-e4f8c172dd36?w=500&q=80',
  'Sandwich':            'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=500&q=80',
  'Momos':               'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?w=500&q=80',
  'Cold Coffee':         'https://images.unsplash.com/photo-1517701550927-30cfcb07071e?w=500&q=80',
  'Veg Roll':            'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=500&q=80',
  'French Fries':        'https://images.unsplash.com/photo-1576107232684-1279f3908594?w=500&q=80',
  // ── Veg Mains ──
  'Butter Paneer':       'https://images.unsplash.com/photo-1589301760014-d929f39ce9b1?w=500&q=80',
  'Mix Vegetable':       'https://images.unsplash.com/photo-1604152135912-04a022e23696?w=500&q=80',
  'Chilli Paneer':       'https://images.unsplash.com/photo-1598514982205-f36b96d1e8d4?w=500&q=80',
  'Channa Masala':       'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=500&q=80',
  'Egg Curry':           'https://images.unsplash.com/photo-1631452180519-c014fe946bc0?w=500&q=80',
  'Butter Chicken':      'https://images.unsplash.com/photo-1603894584373-5ac82b6ae398?w=500&q=80',
  'Dal Fry':             'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=500&q=80',
  'Rice':                'https://images.unsplash.com/photo-1516684732162-798a0062be99?w=500&q=80',
  'Tawa Roti':           'https://images.unsplash.com/photo-1626082895617-2c6cddb9b4f8?w=500&q=80',
  'Tandoori Roti':       'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500&q=80',
  // ── Non Veg ──
  'Chicken Biryani':     'https://images.unsplash.com/photo-1630383249896-424e482df921?w=500&q=80',
  'Mutton Biryani':      'https://images.unsplash.com/photo-1633945274417-4c4d76be3b00?w=500&q=80',
  'Chicken Curry':       'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80',
  'Mutton Curry':        'https://images.unsplash.com/photo-1603894584373-5ac82b6ae398?w=500&q=80',
  'Chicken Tikka Masala':'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80',
  'Keema Matar':         'https://images.unsplash.com/photo-1603894584373-5ac82b6ae398?w=500&q=80',
  'Fish Fry':            'https://images.unsplash.com/photo-1580476262798-bddd9f4b7369?w=500&q=80',
  'Egg Bhurji':          'https://images.unsplash.com/photo-1631452180519-c014fe946bc0?w=500&q=80',
  'Chicken Korma':       'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80',
  'Prawn Masala':        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500&q=80',
  // ── Beverages ──
  'Mango Lassi':         'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=500&q=80',
  'Sweet Lassi':         'https://images.unsplash.com/photo-1571091655789-405eb7a3a3a8?w=500&q=80',
  'Masala Chai':         'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&q=80',
  'Mango Shake':         'https://images.unsplash.com/photo-1553361371-9b22f78e8b1d?w=500&q=80',
  'Banana Shake':        'https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=500&q=80',
  'Oreo Shake':          'https://images.unsplash.com/photo-1572490122747-3e9523c027ac?w=500&q=80',
  'Fresh Lime Soda':     'https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=500&q=80',
  'Watermelon Juice':    'https://images.unsplash.com/photo-1528825871115-3581a5387919?w=500&q=80',
  'Masala Chaas':        'https://images.unsplash.com/photo-1571091655789-405eb7a3a3a8?w=500&q=80',
  // ── Breads ──
  'Butter Naan':         'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80',
  'Garlic Naan':         'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80',
  'Stuffed Kulcha':      'https://images.unsplash.com/photo-1626082895617-2c6cddb9b4f8?w=500&q=80',
  'Aloo Paratha':        'https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=500&q=80',
  'Paneer Paratha':      'https://images.unsplash.com/photo-1645177628172-a94c1f96e6db?w=500&q=80',
  'Laccha Paratha':      'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500&q=80',
  'Missi Roti':          'https://images.unsplash.com/photo-1626082895617-2c6cddb9b4f8?w=500&q=80',
  'Puri (2 pcs)':        'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500&q=80',
  'Rumali Roti':         'https://images.unsplash.com/photo-1626082895617-2c6cddb9b4f8?w=500&q=80',
  'Bhature (2 pcs)':     'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=500&q=80',
  // ── Desserts ──
  'Gulab Jamun (2 pcs)': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80',
  'Rasgulla (2 pcs)':    'https://images.unsplash.com/photo-1545888983-b714c5e9cd7b?w=500&q=80',
  'Kheer':               'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=500&q=80',
  'Gajar Halwa':         'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80',
  'Ice Cream (1 scoop)': 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=500&q=80',
  'Brownie with Ice Cream':'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500&q=80',
  'Jalebi (100g)':       'https://images.unsplash.com/photo-1589301760014-d929f39ce9b1?w=500&q=80',
  'Rabri':               'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=500&q=80',
  'Phirni':              'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=500&q=80',
  'Shahi Tukda':         'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&q=80',
  // ── Soups ──
  'Tomato Soup':         'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
  'Sweet Corn Soup':     'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
  'Hot & Sour Soup':     'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
  'Manchow Soup':        'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
  'Cream of Mushroom Soup':'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
  'Lemon Coriander Soup':'https://images.unsplash.com/photo-1547592180-85f173990554?w=500&q=80',
  // ── Starters ──
  'Paneer Tikka':        'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&q=80',
  'Chicken Tikka':       'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&q=80',
  'Veg Seekh Kebab':     'https://images.unsplash.com/photo-1599487488310-b8e6dce0dab0?w=500&q=80',
  'Chicken Seekh Kebab': 'https://images.unsplash.com/photo-1599487488310-b8e6dce0dab0?w=500&q=80',
  'Hara Bhara Kebab':    'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&q=80',
  'Tandoori Chicken (half)':'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&q=80',
  'Aloo Tikki (2 pcs)':  'https://images.unsplash.com/photo-1589301760014-d929f39ce9b1?w=500&q=80',
  'Onion Pakora':        'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=500&q=80',
  'Spring Rolls (4 pcs)':'https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?w=500&q=80',
  'Dahi Ke Sholay':      'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&q=80',
};

// ─── Render Menu ─────────────────────────────────────────────────────────────
function renderMenu() {
  const grid = document.getElementById('menu-grid');
  const items = menuData[activeCategory] || [];

  grid.innerHTML = items
    .map((item) => {
      const inCart = cart.find((c) => c.menuItemId === item.id);
      const qty = inCart ? inCart.quantity : 0;
      const defaultImg = 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=500&q=80';
      const imgSrc = itemImages[item.name] || defaultImg;

      return `
      <div class="menu-card" id="menu-card-${item.id}">
        <img src="${imgSrc}" alt="${item.name}" class="menu-card__img" loading="lazy" />
        <div class="menu-card__content">
          <div class="menu-card__info">
            <div class="menu-card__name">${item.name}</div>
            <div class="menu-card__price">₹${parseFloat(item.price).toFixed(0)}</div>
          </div>
          <div class="menu-card__actions">
            ${
              qty > 0
                ? `<div class="qty-controls">
                     <button class="qty-btn" onclick="updateQty(${item.id}, -1)">−</button>
                     <span class="qty-value">${qty}</span>
                     <button class="qty-btn" onclick="updateQty(${item.id}, 1)">+</button>
                   </div>`
                : `<button class="menu-card__add-btn" onclick="addToCart(${item.id}, '${item.name.replace(/'/g, "\\'")}', ${item.price})">+</button>`
            }
          </div>
        </div>
      </div>`;
    })
    .join('');

  updateCartBar();
}

// ─── Category Tabs ───────────────────────────────────────────────────────────
function switchCategory(category, btn) {
  activeCategory = category;
  document.querySelectorAll('.menu-tab').forEach((t) => t.classList.remove('active'));
  btn.classList.add('active');
  renderMenu();
}

// ─── Cart Operations ─────────────────────────────────────────────────────────
function addToCart(id, name, price) {
  const existing = cart.find((c) => c.menuItemId === id);
  if (existing) {
    existing.quantity++;
  } else {
    cart.push({ menuItemId: id, name, price: parseFloat(price), quantity: 1 });
  }
  renderMenu();
}

function updateQty(id, delta) {
  const item = cart.find((c) => c.menuItemId === id);
  if (!item) return;
  item.quantity += delta;
  if (item.quantity <= 0) {
    cart = cart.filter((c) => c.menuItemId !== id);
  }
  renderMenu();
}

function updateCartBar() {
  const bar = document.getElementById('cart-bar');
  const count = cart.reduce((sum, c) => sum + c.quantity, 0);
  const total = cart.reduce((sum, c) => sum + c.price * c.quantity, 0);

  if (count > 0) {
    bar.classList.remove('hidden');
    document.getElementById('cart-bar-count').textContent = `${count} item${count !== 1 ? 's' : ''}`;
    document.getElementById('cart-bar-total').textContent = `₹${total.toFixed(0)}`;
  } else {
    bar.classList.add('hidden');
  }
}

// ─── Render Cart ─────────────────────────────────────────────────────────────
function renderCart() {
  const container = document.getElementById('cart-items');
  const emptyEl = document.getElementById('cart-empty');
  const summaryEl = document.getElementById('cart-summary');

  if (cart.length === 0) {
    container.innerHTML = '';
    emptyEl.classList.remove('hidden');
    summaryEl.style.display = 'none';
    return;
  }

  emptyEl.classList.add('hidden');
  summaryEl.style.display = '';

  container.innerHTML = cart
    .map(
      (item) => `
    <div class="cart-item">
      <div class="cart-item__info">
        <div class="cart-item__name">${item.name}</div>
        <div class="cart-item__price">₹${item.price.toFixed(0)} each</div>
      </div>
      <div class="qty-controls">
        <button class="qty-btn" onclick="updateCartQty(${item.menuItemId}, -1)">−</button>
        <span class="qty-value">${item.quantity}</span>
        <button class="qty-btn" onclick="updateCartQty(${item.menuItemId}, 1)">+</button>
      </div>
      <div class="cart-item__total">₹${(item.price * item.quantity).toFixed(0)}</div>
    </div>`
    )
    .join('');

  updateCartSummary();
}

function updateCartQty(id, delta) {
  const item = cart.find((c) => c.menuItemId === id);
  if (!item) return;
  item.quantity += delta;
  if (item.quantity <= 0) {
    cart = cart.filter((c) => c.menuItemId !== id);
  }
  renderCart();
  updateCartBar();
}

function updateCartSummary() {
  const subtotal = cart.reduce((sum, c) => sum + c.price * c.quantity, 0);
  const { discountPercent, discountAmount, total } = calcDiscount(subtotal);

  document.getElementById('cart-subtotal').textContent = `₹${subtotal.toFixed(0)}`;
  document.getElementById('cart-total').textContent = `₹${total.toFixed(0)}`;

  const discRow = document.getElementById('cart-discount-row');
  if (discountPercent > 0) {
    discRow.classList.remove('hidden');
    document.getElementById('cart-discount').textContent = `-₹${discountAmount.toFixed(0)}`;
  } else {
    discRow.classList.add('hidden');
  }
}

// ─── Birthday Discount ──────────────────────────────────────────────────────
function calcDiscount(subtotal) {
  const dobInput = document.getElementById('cust-dob');
  let discountPercent = 0;

  if (dobInput && dobInput.value) {
    const dob = new Date(dobInput.value);
    const today = new Date();
    if (dob.getDate() === today.getDate() && dob.getMonth() === today.getMonth()) {
      discountPercent = 20;
    }
  }

  const discountAmount = (subtotal * discountPercent) / 100;
  const total = subtotal - discountAmount;
  return { discountPercent, discountAmount, total };
}

// ─── Render Checkout ─────────────────────────────────────────────────────────
function renderCheckout() {
  const list = document.getElementById('checkout-items-list');
  const subtotal = cart.reduce((sum, c) => sum + c.price * c.quantity, 0);
  const { total } = calcDiscount(subtotal);

  list.innerHTML = cart
    .map(
      (item) => `
    <div class="checkout-item-row">
      <span>${item.name} × ${item.quantity}</span>
      <span>₹${(item.price * item.quantity).toFixed(0)}</span>
    </div>`
    )
    .join('');

  document.getElementById('checkout-total').textContent = `₹${total.toFixed(0)}`;
}

// ─── Toggle Buttons ──────────────────────────────────────────────────────────
function selectToggle(btn, hiddenInputId) {
  const group = btn.closest('.toggle-group');
  group.querySelectorAll('.toggle-btn').forEach((b) => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(hiddenInputId).value = btn.dataset.value;
}

// ─── Place Order ─────────────────────────────────────────────────────────────
async function placeOrder(e) {
  e.preventDefault();

  const btn = document.getElementById('place-order-btn');
  const btnText = btn.querySelector('.btn__text');
  const btnLoader = btn.querySelector('.btn__loader');

  const name = document.getElementById('cust-name').value.trim();
  const dob = document.getElementById('cust-dob').value;
  const mobile = document.getElementById('cust-mobile').value.trim();
  const orderType = document.getElementById('order-type').value;
  const paymentMethod = document.getElementById('payment-method').value;

  if (!name || !mobile || mobile.length !== 10) {
    alert('Please fill in all required fields correctly.');
    return;
  }

  if (cart.length === 0) {
    alert('Your cart is empty!');
    return;
  }

  btnText.classList.add('hidden');
  btnLoader.classList.remove('hidden');
  btn.disabled = true;

  try {
    const rpRes = await fetch('/api/create-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer: { name, dob: dob || null, mobile },
        items: cart.map((c) => ({ menuItemId: c.menuItemId, quantity: c.quantity }))
      }),
    });

    if (!rpRes.ok) throw new Error('Failed to create payment order');
    const rpData = await rpRes.json();

    const options = {
      key: rpData.key_id,
      amount: rpData.amount.toString(),
      currency: rpData.currency,
      name: 'CS Triplet Eatery',
      description: 'Order Payment',
      order_id: rpData.order_id,
      handler: async function (response) {
        try {
          const finalRes = await fetch('/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              customer: { name, dob: dob || null, mobile },
              items: cart.map((c) => ({ menuItemId: c.menuItemId, quantity: c.quantity })),
              orderType,
              paymentMethod,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_order_id: response.razorpay_order_id,
              razorpay_signature: response.razorpay_signature,
            }),
          });

          if (!finalRes.ok) throw new Error('Failed to finalize order');
          const order = await finalRes.json();

          renderReceipt(order, name, mobile, paymentMethod, response.razorpay_payment_id);
          showSection('receipt-section');

          cart = [];
          document.getElementById('checkout-form').reset();
          document.getElementById('order-type').value = 'dine_in';
          document.getElementById('payment-method').value = 'upi';
        } catch (err) {
          console.error('Finalize order error:', err);
          alert('Payment was successful but order creation failed. Please contact staff.');
        } finally {
          btnText.classList.remove('hidden');
          btnLoader.classList.add('hidden');
          btn.disabled = false;
        }
      },
      prefill: { name, contact: mobile },
      theme: { color: '#f59e0b' },
      modal: {
        ondismiss: function () {
          btnText.classList.remove('hidden');
          btnLoader.classList.add('hidden');
          btn.disabled = false;
        },
      },
    };

    const rzp1 = new Razorpay(options);
    rzp1.open();
  } catch (err) {
    console.error('Order error:', err);
    alert('Failed to initiate payment. Please try again.');
    btnText.classList.remove('hidden');
    btnLoader.classList.add('hidden');
    btn.disabled = false;
  }
}

// ─── Render Receipt ──────────────────────────────────────────────────────────
async function renderReceipt(order, name, mobile, paymentMethod, paymentId) {
  document.getElementById('receipt-order-no').textContent = `#${order.orderNumber}`;
  document.getElementById('receipt-name').textContent = name;
  document.getElementById('receipt-mobile').textContent = mobile;
  document.getElementById('receipt-datetime').textContent = new Date(order.createdAt).toLocaleString('en-IN');

  const typeLabel = order.orderType === 'dine_in' ? 'Dine In' : 'Takeaway';
  document.getElementById('receipt-type').textContent = typeLabel;

  const seatWrapper = document.getElementById('receipt-seat-wrapper');
  if (order.seatNumber) {
    seatWrapper.style.display = '';
    document.getElementById('receipt-seat-no').textContent = order.seatNumber;
  } else {
    seatWrapper.style.display = 'none';
  }

  const payLabels = { cash: 'Cash', card: 'Card', upi: 'Razorpay UPI' };
  document.getElementById('receipt-payment').textContent = payLabels[paymentMethod] || paymentMethod;
  document.getElementById('receipt-payment-id').textContent = paymentId || '—';

  // Flatten all categories into one lookup map: id -> item
  const allItems = Object.values(menuData).flat();
  const itemMap = {};
  allItems.forEach((m) => { itemMap[m.id] = m; });

  const itemsContainer = document.getElementById('receipt-items');
  itemsContainer.innerHTML = order.items
    .map((item) => {
      const menuItem = itemMap[item.menuItemId] || {};
      return `
    <div class="receipt-item-row">
      <span>${menuItem.name || 'Item'} × ${item.quantity}</span>
      <span>₹${parseFloat(item.lineTotal).toFixed(0)}</span>
    </div>`;
    })
    .join('');

  document.getElementById('receipt-subtotal').textContent = `₹${parseFloat(order.subtotal).toFixed(0)}`;
  document.getElementById('receipt-total').textContent = `₹${parseFloat(order.total).toFixed(0)}`;

  const discountRow = document.getElementById('receipt-discount-row');
  const birthdayBanner = document.getElementById('receipt-birthday-banner');
  if (order.discountPercent > 0) {
    const discountAmount = (parseFloat(order.subtotal) * order.discountPercent) / 100;
    discountRow.classList.remove('hidden');
    document.getElementById('receipt-discount').textContent = `-₹${discountAmount.toFixed(0)}`;
    birthdayBanner.classList.remove('hidden');
  } else {
    discountRow.classList.add('hidden');
    birthdayBanner.classList.add('hidden');
  }

  const qrSection = document.getElementById('receipt-qr-section');
  if (paymentMethod === 'upi') {
    try {
      const qrRes = await fetch(`/api/qr/${order.orderId}`);
      const qrData = await qrRes.json();
      document.getElementById('receipt-qr-img').src = qrData.qr;
      qrSection.classList.remove('hidden');
    } catch (err) {
      qrSection.classList.add('hidden');
    }
  } else {
    qrSection.classList.add('hidden');
  }
}

// ─── New Order ───────────────────────────────────────────────────────────────
function newOrder() {
  cart = [];
  closeOverlay();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ─── DOB change listener for live discount calc ─────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  fetchMenu();

  const dobInput = document.getElementById('cust-dob');
  if (dobInput) {
    dobInput.addEventListener('change', () => {
      updateCartSummary();
      renderCheckout();
    });
  }
});


