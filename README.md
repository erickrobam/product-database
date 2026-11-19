# Product Database

A simple MySQL database for storing product information, with a Python utility to export all products to Excel.

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
- Python 3.10 or newer
- A MySQL user with permission to read the `product` table

## 1. Create the database

Run the SQL script from the repository root:

```bash
mysql -u your_username -p < sql/create_database.sql
```

This creates the database and table if they do not already exist.

## 2. Install the Python dependencies

Create and activate a virtual environment (recommended), then run:

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\\Scripts\\Activate.ps1
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## 3. Configure the MySQL connection

Copy `.env.example` to a new file named `.env` and enter your MySQL connection details:

```dotenv
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=product_database
```

The `.env` file is ignored by Git, so your local database password is not committed to the repository. Do not commit real credentials.

The MySQL account needs `SELECT` permission on `product_database.product`.

## 4. Export all products to Excel

From the repository root, run:

```bash
python src/export_products.py
```

The script reads every row from the `product` table and creates `products_export.xlsx` in the current directory. The spreadsheet contains Product ID, Product name, Product date, and Product value. It includes a header row, filters, frozen headers, and readable column widths.

To choose a different output path:

```bash
python src/export_products.py --output reports/all_products.xlsx
```

If the table is empty, the script still creates an Excel file containing the column headers.

## Example SQL

```sql
USE product_database;

INSERT INTO product (name_product, date_product, value_product)
VALUES ('Example product', '2026-11-18', 29.90);

SELECT product_id, name_product, date_product, value_product
FROM product;
```

## Project structure

```text
product-database/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── sql/
│   └── create_database.sql
└── src/
    └── export_products.py
```
