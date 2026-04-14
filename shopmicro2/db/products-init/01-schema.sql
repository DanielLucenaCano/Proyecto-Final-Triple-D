CREATE DATABASE IF NOT EXISTS products_db;
USE products_db;

CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  description TEXT,
  price DECIMAL(10,2) NOT NULL,
  stock INT NOT NULL DEFAULT 0
);

INSERT INTO products (name, description, price, stock)
VALUES
  ('Mechanical Keyboard', 'RGB mechanical keyboard for gaming', 79.99, 12),
  ('Monitor 27 inch', 'QHD IPS monitor for productivity', 229.00, 7),
  ('Wireless Mouse', 'Ergonomic rechargeable wireless mouse', 39.50, 18);
