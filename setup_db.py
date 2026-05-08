"""
Database Setup Script
Run this once to create tables and seed menu data.
"""
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "12345"),
}

print("Connecting to MySQL...")
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

print("Creating database...")
cursor.execute("CREATE DATABASE IF NOT EXISTS restaurant")
cursor.execute("USE restaurant")

print("Creating tables...")

cursor.execute("""
CREATE TABLE IF NOT EXISTS menu_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category ENUM('fast_food', 'regular') NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  dob DATE DEFAULT NULL,
  mobile VARCHAR(15) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_number INT NOT NULL,
  customer_id INT NOT NULL,
  order_type ENUM('dine_in', 'takeaway') NOT NULL,
  seat_number INT DEFAULT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  discount_percent DECIMAL(5,2) DEFAULT 0,
  total DECIMAL(10,2) NOT NULL,
  payment_method ENUM('cash', 'card', 'upi') NOT NULL,
  payment_id VARCHAR(255) DEFAULT NULL,
  status ENUM('pending', 'preparing', 'ready', 'completed') DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (customer_id) REFERENCES customers(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  menu_item_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  line_total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
)
""")

print("Seeding menu items...")

# Check if menu items already exist
cursor.execute("SELECT COUNT(*) FROM menu_items")
count = cursor.fetchone()[0]

if count == 0:
    menu_items = [
        ('Pasta',         'fast_food', 200),
        ('Pizza',         'fast_food', 250),
        ('Burger',        'fast_food',  50),
        ('Fried Rice',    'fast_food', 180),
        ('Manchurian',    'fast_food', 150),
        ('Sandwich',      'fast_food',  40),
        ('Momos',         'fast_food',  30),
        ('Cold Coffee',   'fast_food',  80),
        ('Veg Roll',      'fast_food', 120),
        ('French Fries',  'fast_food',  40),
        ('Butter Paneer',  'regular', 300),
        ('Mix Vegetable',  'regular', 150),
        ('Chilli Paneer',  'regular', 200),
        ('Channa Masala',  'regular', 155),
        ('Egg Curry',      'regular', 180),
        ('Butter Chicken', 'regular', 350),
        ('Dal Fry',        'regular', 120),
        ('Rice',           'regular',  60),
        ('Tawa Roti',      'regular',   8),
        ('Tandoori Roti',  'regular',  12),
    ]
    cursor.executemany(
        "INSERT INTO menu_items (name, category, price) VALUES (%s, %s, %s)",
        menu_items,
    )
    print(f"  ✅ Inserted {len(menu_items)} menu items")
else:
    print(f"  ℹ️  Menu already has {count} items, skipping seed")

conn.commit()
cursor.close()
conn.close()

print()
print("  ✅ Database setup complete!")
print("  ▶  Now run: python3 app.py")
print()
