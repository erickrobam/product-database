# Product Database

A simple MySQL database for storing product information.

## Database schema

The project creates a database named `product_database` with one table named `product`.

| Column | Type | Description |
| --- | --- | --- |
| `product_id` | `BIGINT UNSIGNED` | Auto-incrementing primary key |
| `name_product` | `VARCHAR(255)` | Product name (required) |
| `date_product` | `DATE` | Product date |
| `value_product` | `DECIMAL(12,2)` | Product value (required) |

## Requirements

- MySQL 8.0 or compatible MySQL server
- A MySQL client, such as the `mysql` command-line client or MySQL Workbench

## Create the database

Run the SQL script from the repository root:

```bash
mysql -u your_username -p < sql/create_database.sql
```

Replace `your_username` with your MySQL username. The script creates the database and table if they do not already exist.

## Example usage

After running the creation script, connect to the database:

```sql
USE product_database;

INSERT INTO product (name_product, date_product, value_product)
VALUES ('Example product', '2026-11-18', 29.90);

SELECT product_id, name_product, date_product, value_product
FROM product;
```

The product ID is generated automatically. Store monetary values in `DECIMAL`, not floating-point types, to avoid common rounding issues.

## Project structure

```text
product-database/
├── README.md
├── .gitignore
└── sql/
    └── create_database.sql
```
