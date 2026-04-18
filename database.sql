CREATE DATABASE IF NOT EXISTS crud_vehiculos;
USE crud_vehiculos;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_users_email (email)
);

CREATE TABLE IF NOT EXISTS vehiculos (
    id VARCHAR(36) NOT NULL,
    placa VARCHAR(10) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(30) NOT NULL,
    version VARCHAR(50) NOT NULL,
    color VARCHAR(30) NOT NULL,
    num_puestos INT NOT NULL,
    num_puertas INT NOT NULL,
    combustible VARCHAR(20) NOT NULL,
    kilometros INT NOT NULL,
    cilindraje INT NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_vehiculos_placa (placa)
);

INSERT INTO users (id, name, email, password, role, status, created_at, updated_at)
VALUES (
    'admin-seed-001',
    'Administrador',
    'admin@demo.com',
    '$2y$10$CAqN/fQDDJp7s5xX9U.BdufQqsOoC1M72gYPmWaWQXwXJrmsRiyJq',
    'ADMIN',
    'ACTIVE',
    NOW(),
    NOW()
);
-- contraseña: Admin123*
