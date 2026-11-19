-- Create the product database and its product table.
-- Run with: mysql -u your_username -p < sql/create_database.sql

CREATE DATABASE IF NOT EXISTS product_database
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE product_database;

CREATE TABLE IF NOT EXISTS product (
    product_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name_product VARCHAR(255) NOT NULL,
    date_product DATE NULL,
    value_product DECIMAL(12, 2) NOT NULL,
    PRIMARY KEY (product_id)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
