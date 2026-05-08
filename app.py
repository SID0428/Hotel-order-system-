"""
CS Triplet Eatery — Flask Backend Server
=========================================
A full-stack restaurant ordering application.

Run:  python app.py
Visit: http://localhost:3000
Admin: http://localhost:3000/admin
"""

import os
import io
import base64
import random
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, request, send_from_directory, abort
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling
import razorpay

# ─── Config ──────────────────────────────────────────────────────────────────
load_dotenv()

app = Flask(__name__, static_folder="public", static_url_path="")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "12345"),
    "database": os.getenv("DB_NAME", "siddharth"),
}

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
PORT = int(os.getenv("PORT", 3000))

if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
else:
    razorpay_client = None

# ─── Database Connection Pool ───────────────────────────────────────────────
try:
    pool = pooling.MySQLConnectionPool(
        pool_name="eatery_pool",
        pool_size=5,
        pool_reset_session=True,
        **DB_CONFIG,
    )
    print("  ✅ Database connection pool created")
except mysql.connector.Error as err:
    print(f"  ⚠️  Database connection failed: {err}")
    print("  ⚠️  Server will start but API calls will fail. Run schema.sql first.")
    pool = None


def get_db():
    """Get a connection from the pool."""
    if pool is None:
        raise Exception("Database not connected")
    return pool.get_connection()


# ═════════════════════════════════════════════════════════════════════════════
# STATIC FILE ROUTES
# ═════════════════════════════════════════════════════════════════════════════

@app.route("/")
def serve_index():
    return send_from_directory("public", "index.html")


@app.route("/admin")
def serve_admin():
    return send_from_directory("public", "admin.html")


# Serve all static files from /public
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("public", path)


# ═════════════════════════════════════════════════════════════════════════════
# API: MENU
# ═════════════════════════════════════════════════════════════════════════════

@app.route("/api/menu", methods=["GET"])
def get_menu():
    """Fetch all available menu items, grouped by category."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, category, price FROM menu_items "
            "WHERE is_available = TRUE ORDER BY category, id"
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert Decimal to float for JSON serialization
        for row in rows:
            row["price"] = float(row["price"])

        menu = {
            "fast_food": [r for r in rows if r["category"] == "fast_food"],
            "regular": [r for r in rows if r["category"] == "regular"],
        }
        return jsonify(menu)

    except Exception as e:
        print(f"Error fetching menu: {e}")
        return jsonify({"error": "Failed to fetch menu"}), 500


# ═════════════════════════════════════════════════════════════════════════════
# API: ORDERS
# ═════════════════════════════════════════════════════════════════════════════

@app.route("/api/orders", methods=["POST"])
def place_order():
    """Place a new order."""
    conn = None
    try:
        data = request.get_json()
        customer = data.get("customer", {})
        items = data.get("items", [])
        order_type = data.get("orderType")
        payment_method = data.get("paymentMethod")

        # Validate
        if not customer or not items or not order_type or not payment_method:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # 1. Create customer
        cursor.execute(
            "INSERT INTO customers (name, dob, mobile) VALUES (%s, %s, %s)",
            (customer["name"], customer.get("dob") or None, customer["mobile"]),
        )
        customer_id = cursor.lastrowid

        # 2. Fetch menu prices
        menu_ids = [item["menuItemId"] for item in items]
        format_strings = ",".join(["%s"] * len(menu_ids))
        cursor.execute(
            f"SELECT id, price FROM menu_items WHERE id IN ({format_strings})",
            tuple(menu_ids),
        )
        price_rows = cursor.fetchall()
        price_map = {r["id"]: float(r["price"]) for r in price_rows}

        # 3. Calculate totals
        subtotal = 0.0
        line_items = []
        for item in items:
            unit_price = price_map.get(item["menuItemId"], 0)
            line_total = unit_price * item["quantity"]
            subtotal += line_total
            line_items.append({
                **item,
                "unitPrice": unit_price,
                "lineTotal": line_total,
            })

        # 4. Birthday discount
        discount_percent = 0
        dob_str = customer.get("dob")
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d")
                today = datetime.now()
                if dob.day == today.day and dob.month == today.month:
                    discount_percent = 20
            except ValueError:
                pass

        discount_amount = (subtotal * discount_percent) / 100
        total = subtotal - discount_amount

        return {"subtotal": subtotal, "total": total, "discount_percent": discount_percent, "customer_id": customer_id, "line_items": line_items}
    except Exception as e:
        raise e

@app.route("/api/create-payment", methods=["POST"])
def create_payment():
    """Create a Razorpay order for checkout."""
    if not razorpay_client:
        return jsonify({"error": "Razorpay keys not configured"}), 500

    conn = None
    try:
        data = request.get_json()
        
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # We only need to calculate the total here. 
        # We will roll back any customer insertion to avoid duplicates, 
        # or we just skip inserting the customer for now. 
        # Let's extract the calculate logic cleanly.
        
        # Fetch menu prices
        items = data.get("items", [])
        customer = data.get("customer", {})
        if not items:
            return jsonify({"error": "Cart is empty"}), 400
            
        menu_ids = [item["menuItemId"] for item in items]
        format_strings = ",".join(["%s"] * len(menu_ids))
        cursor.execute(
            f"SELECT id, price FROM menu_items WHERE id IN ({format_strings})",
            tuple(menu_ids),
        )
        price_rows = cursor.fetchall()
        price_map = {r["id"]: float(r["price"]) for r in price_rows}

        subtotal = sum(price_map.get(item["menuItemId"], 0) * item["quantity"] for item in items)
        
        discount_percent = 0
        dob_str = customer.get("dob")
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d")
                today = datetime.now()
                if dob.day == today.day and dob.month == today.month:
                    discount_percent = 20
            except ValueError:
                pass

        discount_amount = (subtotal * discount_percent) / 100
        total = subtotal - discount_amount

        cursor.close()
        conn.close()

        # Create Razorpay order
        amount_in_paise = int(total * 100)
        rp_order = razorpay_client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"rcpt_{random.randint(1000,9999)}",
            "payment_capture": 1
        })
        
        return jsonify({
            "order_id": rp_order["id"],
            "amount": amount_in_paise,
            "currency": "INR",
            "key_id": RAZORPAY_KEY_ID
        })
    except Exception as e:
        if conn:
            conn.close()
        print(f"Error creating payment: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/orders", methods=["POST"])
def create_order():
    """Verify Razorpay payment and place order."""
    conn = None
    try:
        data = request.get_json()
        customer = data.get("customer", {})
        items = data.get("items", [])
        order_type = data.get("orderType")
        payment_method = data.get("paymentMethod")
        
        rp_payment_id = data.get("razorpay_payment_id")
        rp_order_id = data.get("razorpay_order_id")
        rp_signature = data.get("razorpay_signature")

        if payment_method == "upi" and razorpay_client:
            # Verify Signature
            try:
                razorpay_client.utility.verify_payment_signature({
                    'razorpay_order_id': rp_order_id,
                    'razorpay_payment_id': rp_payment_id,
                    'razorpay_signature': rp_signature
                })
            except Exception as e:
                return jsonify({"error": "Invalid payment signature"}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # 1. Create customer
        cursor.execute(
            "INSERT INTO customers (name, dob, mobile) VALUES (%s, %s, %s)",
            (customer["name"], customer.get("dob") or None, customer["mobile"]),
        )
        customer_id = cursor.lastrowid

        # 2. Fetch menu prices
        menu_ids = [item["menuItemId"] for item in items]
        format_strings = ",".join(["%s"] * len(menu_ids))
        cursor.execute(
            f"SELECT id, price FROM menu_items WHERE id IN ({format_strings})",
            tuple(menu_ids),
        )
        price_rows = cursor.fetchall()
        price_map = {r["id"]: float(r["price"]) for r in price_rows}

        # 3. Calculate totals
        subtotal = 0.0
        line_items = []
        for item in items:
            unit_price = price_map.get(item["menuItemId"], 0)
            line_total = unit_price * item["quantity"]
            subtotal += line_total
            line_items.append({
                **item,
                "unitPrice": unit_price,
                "lineTotal": line_total,
            })

        # 4. Birthday discount
        discount_percent = 0
        dob_str = customer.get("dob")
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d")
                today = datetime.now()
                if dob.day == today.day and dob.month == today.month:
                    discount_percent = 20
            except ValueError:
                pass

        discount_amount = (subtotal * discount_percent) / 100
        total = subtotal - discount_amount

        # 5. Generate order & seat numbers
        order_number = random.randint(1, 999)
        seat_number = random.randint(1000, 9999) if order_type == "dine_in" else None

        # 6. Insert order
        cursor.execute(
            "INSERT INTO orders "
            "(order_number, customer_id, order_type, seat_number, subtotal, discount_percent, total, payment_method, payment_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (order_number, customer_id, order_type, seat_number,
             subtotal, discount_percent, total, payment_method, rp_payment_id),
        )
        order_id = cursor.lastrowid

        # 7. Insert order items
        for item in line_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price, line_total) "
                "VALUES (%s, %s, %s, %s, %s)",
                (order_id, item["menuItemId"], item["quantity"],
                 item["unitPrice"], item["lineTotal"]),
            )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "orderId": order_id,
            "orderNumber": order_number,
            "seatNumber": seat_number,
            "customerName": customer["name"],
            "orderType": order_type,
            "paymentMethod": payment_method,
            "subtotal": subtotal,
            "discountPercent": discount_percent,
            "total": total,
            "items": line_items,
            "createdAt": datetime.now().isoformat(),
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        print(f"Error placing order: {e}")
        return jsonify({"error": "Failed to place order"}), 500


@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Get order details (receipt)."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT o.*, c.name AS customer_name, c.dob, c.mobile "
            "FROM orders o JOIN customers c ON o.customer_id = c.id "
            "WHERE o.id = %s",
            (order_id,),
        )
        order = cursor.fetchone()

        if not order:
            cursor.close()
            conn.close()
            return jsonify({"error": "Order not found"}), 404

        # Convert types for JSON
        for key in ("subtotal", "discount_percent", "total"):
            if order.get(key) is not None:
                order[key] = float(order[key])
        if order.get("created_at"):
            order["created_at"] = order["created_at"].isoformat()
        if order.get("dob"):
            order["dob"] = order["dob"].isoformat()

        cursor.execute(
            "SELECT oi.*, mi.name AS item_name "
            "FROM order_items oi JOIN menu_items mi ON oi.menu_item_id = mi.id "
            "WHERE oi.order_id = %s",
            (order_id,),
        )
        items = cursor.fetchall()
        for item in items:
            for key in ("unit_price", "line_total"):
                if item.get(key) is not None:
                    item[key] = float(item[key])

        order["items"] = items
        cursor.close()
        conn.close()

        return jsonify(order)

    except Exception as e:
        print(f"Error fetching order: {e}")
        return jsonify({"error": "Failed to fetch order"}), 500


# ═════════════════════════════════════════════════════════════════════════════
# API: QR CODE
# ═════════════════════════════════════════════════════════════════════════════

@app.route("/api/qr/<int:order_id>", methods=["GET"])
def generate_qr(order_id):
    """Generate UPI QR code for an order."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT total FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        cursor.close()
        conn.close()

        if not order:
            return jsonify({"error": "Order not found"}), 404

        amount = float(order["total"])
        upi_url = (
            f"upi://pay?pa={UPI_ID}"
            f"&pn={UPI_NAME}"
            f"&am={amount}"
            f"&cu=INR"
        )

        # Generate QR code as base64 data URL
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(upi_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#f5f5f5", back_color="#161616")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        data_url = f"data:image/png;base64,{b64}"

        return jsonify({"qr": data_url, "upiUrl": upi_url, "amount": amount})

    except Exception as e:
        print(f"Error generating QR: {e}")
        return jsonify({"error": "Failed to generate QR code"}), 500


# ═════════════════════════════════════════════════════════════════════════════
# API: ADMIN
# ═════════════════════════════════════════════════════════════════════════════

@app.route("/api/admin/orders", methods=["GET"])
def admin_get_orders():
    """List all orders for admin dashboard."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT o.*, c.name AS customer_name, c.mobile "
            "FROM orders o JOIN customers c ON o.customer_id = c.id "
            "ORDER BY o.created_at DESC"
        )
        orders = cursor.fetchall()

        for order in orders:
            # Convert types
            for key in ("subtotal", "discount_percent", "total"):
                if order.get(key) is not None:
                    order[key] = float(order[key])
            if order.get("created_at"):
                order["created_at"] = order["created_at"].isoformat()

            # Fetch items for each order
            cursor.execute(
                "SELECT oi.*, mi.name AS item_name "
                "FROM order_items oi JOIN menu_items mi ON oi.menu_item_id = mi.id "
                "WHERE oi.order_id = %s",
                (order["id"],),
            )
            items = cursor.fetchall()
            for item in items:
                for key in ("unit_price", "line_total"):
                    if item.get(key) is not None:
                        item[key] = float(item[key])
            order["items"] = items

        cursor.close()
        conn.close()

        return jsonify(orders)

    except Exception as e:
        print(f"Error fetching admin orders: {e}")
        return jsonify({"error": "Failed to fetch orders"}), 500


@app.route("/api/admin/orders/<int:order_id>/status", methods=["PATCH"])
def admin_update_status(order_id):
    """Update order status."""
    try:
        data = request.get_json()
        status = data.get("status")
        valid_statuses = ["pending", "preparing", "ready", "completed"]

        if status not in valid_statuses:
            return jsonify({"error": "Invalid status"}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (status, order_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "status": status})

    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify({"error": "Failed to update status"}), 500


# ═════════════════════════════════════════════════════════════════════════════
# RUN SERVER
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print()
    print("  🍽️  CS Triplet Eatery server running at http://localhost:{}".format(PORT))
    print("  📋 Admin dashboard at http://localhost:{}/admin".format(PORT))
    print()
    app.run(host="0.0.0.0", port=PORT, debug=True)
