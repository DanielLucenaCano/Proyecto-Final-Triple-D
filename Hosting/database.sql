CREATE DATABASE IF NOT EXISTS hosting_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hosting_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    vcpu INT NOT NULL,
    ram INT NOT NULL,
    ssd INT NOT NULL,
    hdd INT NOT NULL,
    bandwidth INT NOT NULL,
    windows_server TINYINT(1) DEFAULT 0,
    ip_estatica TINYINT(1) DEFAULT 0,
    backup TINYINT(1) DEFAULT 0,
    firewall TINYINT(1) DEFAULT 0,
    panel_control TINYINT(1) DEFAULT 0,
    precio_base DECIMAL(10,2) NOT NULL,
    precio_total DECIMAL(10,2) NOT NULL,
    estado ENUM('activo', 'detenido') DEFAULT 'detenido',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_servers_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
