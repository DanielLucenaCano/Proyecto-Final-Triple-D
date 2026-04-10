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
    ('Teclat mecànic', 'Teclat gaming amb retroil·luminació RGB', 79.99, 12),
    ('Monitor 27 polzades', 'Pantalla IPS QHD per a productivitat', 229.00, 7),
    ('Ratolí sense fils', 'Ratolí ergonòmic amb bateria recarregable', 39.50, 18)
ON DUPLICATE KEY UPDATE name = VALUES(name);

