/* ═══════════════════════════════════════════════════════════════════════════
   CS Triplet Eatery — Admin Dashboard Logic
   ═══════════════════════════════════════════════════════════════════════════ */

let allOrders = [];
let activeFilter = 'all';

// ─── Load Orders ─────────────────────────────────────────────────────────────
async function loadOrders() {
  const list = document.getElementById('orders-list');
  list.innerHTML = '<div class="orders-empty"><p>Loading orders...</p></div>';

  try {
    const res = await fetch('/api/admin/orders');
    allOrders = await res.json();
    renderOrders();
    updateStats();
  } catch (err) {
    console.error('Failed to load orders:', err);
    list.innerHTML = '<div class="orders-empty"><p>Could not load orders. Is the server running?</p></div>';
  }
}

// ─── Render Orders ───────────────────────────────────────────────────────────
function renderOrders() {
  const list = document.getElementById('orders-list');
  const filtered =
    activeFilter === 'all' ? allOrders : allOrders.filter((o) => o.status === activeFilter);

  if (filtered.length === 0) {
    list.innerHTML = '<div class="orders-empty"><p>No orders found.</p></div>';
    return;
  }

  list.innerHTML = filtered
    .map(
      (order) => `
    <div class="order-card" onclick="openDrawer(${order.id})">
      <div class="order-card__number">#${order.order_number}</div>
      <div class="order-card__info">
        <div class="order-card__customer">${order.customer_name}</div>
        <div class="order-card__meta">
          <span>${order.order_type === 'dine_in' ? '🍽️ Dine In' : '📦 Takeaway'}</span>
          <span>${formatPayment(order.payment_method)}</span>
          <span>${formatTime(order.created_at)}</span>
        </div>
      </div>
      <span class="status-badge status-badge--${order.status}">${order.status}</span>
      <div class="order-card__total">₹${parseFloat(order.total).toFixed(0)}</div>
    </div>`
    )
    .join('');
}

// ─── Update Stats ────────────────────────────────────────────────────────────
function updateStats() {
  document.getElementById('stat-total').textContent = allOrders.length;
  document.getElementById('stat-pending').textContent = allOrders.filter(
    (o) => o.status === 'pending'
  ).length;
  document.getElementById('stat-preparing').textContent = allOrders.filter(
    (o) => o.status === 'preparing'
  ).length;
  document.getElementById('stat-ready').textContent = allOrders.filter(
    (o) => o.status === 'ready'
  ).length;

  const revenue = allOrders
    .filter((o) => o.status === 'completed')
    .reduce((sum, o) => sum + parseFloat(o.total), 0);
  document.getElementById('stat-revenue').textContent = `₹${revenue.toFixed(0)}`;
}

// ─── Filter Tabs ─────────────────────────────────────────────────────────────
function filterOrders(filter, btn) {
  activeFilter = filter;
  document.querySelectorAll('.filter-tab').forEach((t) => t.classList.remove('active'));
  btn.classList.add('active');
  renderOrders();
}

// ─── Drawer ──────────────────────────────────────────────────────────────────
function openDrawer(orderId) {
  const order = allOrders.find((o) => o.id === orderId);
  if (!order) return;

  document.getElementById('drawer-title').textContent = `Order #${order.order_number}`;

  const body = document.getElementById('drawer-body');
  const itemsHtml = (order.items || [])
    .map(
      (item) =>
        `<div class="drawer-row"><span>${item.item_name} × ${item.quantity}</span><span>₹${parseFloat(item.line_total).toFixed(0)}</span></div>`
    )
    .join('');

  const discountHtml =
    parseFloat(order.discount_percent) > 0
      ? `<div class="drawer-row" style="color:#22c55e"><span>🎂 Birthday Discount (${order.discount_percent}%)</span><span>-₹${((parseFloat(order.subtotal) * parseFloat(order.discount_percent)) / 100).toFixed(0)}</span></div>`
      : '';

  const statusButtons = ['pending', 'preparing', 'ready', 'completed']
    .map(
      (s) =>
        `<button class="status-btn ${s === order.status ? 'active-status' : ''}" onclick="updateStatus(${order.id}, '${s}')">${s.charAt(0).toUpperCase() + s.slice(1)}</button>`
    )
    .join('');

  body.innerHTML = `
    <div class="drawer-section">
      <div class="drawer-section__title">Customer</div>
      <div class="drawer-row"><span>Name</span><span>${order.customer_name}</span></div>
      <div class="drawer-row"><span>Mobile</span><span>${order.mobile}</span></div>
      <div class="drawer-row"><span>Type</span><span>${order.order_type === 'dine_in' ? 'Dine In' : 'Takeaway'}</span></div>
      ${order.seat_number ? `<div class="drawer-row"><span>Seat</span><span>${order.seat_number}</span></div>` : ''}
      <div class="drawer-row"><span>Payment</span><span>${formatPayment(order.payment_method)}</span></div>
      <div class="drawer-row"><span>Time</span><span>${formatTime(order.created_at)}</span></div>
    </div>

    <div class="drawer-divider"></div>

    <div class="drawer-section">
      <div class="drawer-section__title">Items</div>
      ${itemsHtml}
    </div>

    <div class="drawer-divider"></div>

    <div class="drawer-section">
      <div class="drawer-row"><span>Subtotal</span><span>₹${parseFloat(order.subtotal).toFixed(0)}</span></div>
      ${discountHtml}
      <div class="drawer-total"><span>Total</span><span>₹${parseFloat(order.total).toFixed(0)}</span></div>
    </div>

    <div class="drawer-divider"></div>

    <div class="drawer-section">
      <div class="drawer-section__title">Update Status</div>
      <div class="drawer-status-btns">${statusButtons}</div>
    </div>
  `;

  document.getElementById('drawer-overlay').classList.add('open');
  document.getElementById('order-drawer').classList.add('open');
}

function closeDrawer() {
  document.getElementById('drawer-overlay').classList.remove('open');
  document.getElementById('order-drawer').classList.remove('open');
}

// ─── Update Status ───────────────────────────────────────────────────────────
async function updateStatus(orderId, status) {
  try {
    await fetch(`/api/admin/orders/${orderId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });

    // Update local data
    const order = allOrders.find((o) => o.id === orderId);
    if (order) order.status = status;

    renderOrders();
    updateStats();
    openDrawer(orderId); // refresh drawer
  } catch (err) {
    console.error('Failed to update status:', err);
    alert('Failed to update order status.');
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────────────
function formatPayment(method) {
  const labels = { cash: '💵 Cash', card: '💳 Card', upi: '📱 UPI' };
  return labels[method] || method;
}

function formatTime(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleString('en-IN', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// ─── Init ────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', loadOrders);

// Auto-refresh every 30 seconds
setInterval(loadOrders, 30000);
