-- CS Triplet Eatery Database Schema
-- Run: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS siddharth;
USE siddharth;

-- ============================================
-- Menu Items
-- ============================================
CREATE TABLE IF NOT EXISTS menu_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category ENUM('fast_food', 'regular') NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Customers
-- ============================================
CREATE TABLE IF NOT EXISTS customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  dob DATE DEFAULT NULL,
  mobile VARCHAR(15) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Orders
-- ============================================
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
);

-- ============================================
-- Order Items (line items per order)
-- ============================================
CREATE TABLE IF NOT EXISTS order_items (
  id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  menu_item_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  line_total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);

-- ============================================
-- Seed Menu Items (from original script)
-- ============================================
INSERT INTO menu_items (name, category, price) VALUES
  -- Fast Food
  ('Pasta',         'fast_food', 200.00),
  ('Pizza',         'fast_food', 250.00),
  ('Burger',        'fast_food',  50.00),
  ('Fried Rice',    'fast_food', 180.00),
  ('Manchurian',    'fast_food', 150.00),
  ('Sandwich',      'fast_food',  40.00),
  ('Momos',         'fast_food',  30.00),
  ('Cold Coffee',   'fast_food',  80.00),
  ('Veg Roll',      'fast_food', 120.00),
  ('French Fries',  'fast_food',  40.00),
  -- Regular
  ('Butter Paneer',  'regular', 300.00),
  ('Mix Vegetable',  'regular', 150.00),
  ('Chilli Paneer',  'regular', 200.00),
  ('Channa Masala',  'regular', 155.00),
  ('Egg Curry',      'regular', 180.00),
  ('Butter Chicken', 'regular', 350.00),
  ('Dal Fry',        'regular', 120.00),
  ('Rice',           'regular',  60.00),
  ('Tawa Roti',      'regular',   8.00),
  ('Tandoori Roti',  'regular',  12.00)
ON DUPLICATE KEY UPDATE name=name;
