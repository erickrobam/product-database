"""Export every row in the MySQL product table to an Excel workbook."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter


COLUMNS = [
    ("product_id", "Product ID"),
    ("name_product", "Product name"),
    ("date_product", "Product date"),
    ("value_product", "Product value"),
]


def load_database_settings() -> dict:
    """Load database settings from environment variables or a local .env file."""
    load_dotenv()

    required = ("MYSQL_USER", "MYSQL_PASSWORD")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ValueError(
            "Missing database setting(s): "
            + ", ".join(missing)
            + ". Copy .env.example to .env and fill in your MySQL credentials."
        )

    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.environ["MYSQL_USER"],
        "password": os.environ["MYSQL_PASSWORD"],
        "database": os.getenv("MYSQL_DATABASE", "product_database"),
    }


def fetch_products(settings: dict) -> list[dict]:
    """Read all products from the database."""
    connection = mysql.connector.connect(**settings)
    try:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT product_id, name_product, date_product, value_product
                FROM product
                ORDER BY product_id
                """
            )
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()


def write_excel(products: list[dict], output_path: Path) -> None:
    """Write products to a formatted Excel workbook."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Products"

    headers = [label for _, label in COLUMNS]
    sheet.append(headers)

    for product in products:
        sheet.append([product[column] for column, _ in COLUMNS])

    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in sheet[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = header_fill

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions

    widths = (14, 32, 18, 18)
    for index, width in enumerate(widths, start=1):
        sheet.column_dimensions[get_column_letter(index)].width = width

    for row in sheet.iter_rows(min_row=2):
        row[2].number_format = "yyyy-mm-dd"
        row[3].number_format = '#,##0.00'

    workbook.save(output_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export all products from MySQL to an Excel (.xlsx) file."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("products_export.xlsx"),
        help="Excel output path (default: products_export.xlsx)",
    )
    args = parser.parse_args()

    try:
        settings = load_database_settings()
        products = fetch_products(settings)
        write_excel(products, args.output)
    except (ValueError, mysql.connector.Error, OSError) as error:
        print(f"Export failed: {error}", file=sys.stderr)
        return 1

    print(f"Exported {len(products)} product(s) to: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
