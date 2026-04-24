#!/usr/bin/env python3
"""
Load all CSV files into DuckDB OLAP database.
"""
import duckdb
import os

CSV_DIR = "data/csv"
DB_PATH = "data/patissier.duckdb"

TABLES = [
    "dim_date",
    "dim_channel",
    "dim_warehouse",
    "dim_store",
    "dim_product",
    "dim_customer",
    "fact_sales",
    "fact_orders",
    "fact_inventory_snapshot",
    "fact_returns",
    "fact_support_tickets",
]

def setup():
    # Remove existing DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[*] Removed existing {DB_PATH}")

    con = duckdb.connect(DB_PATH)
    print(f"[*] Connected to {DB_PATH}\n")

    for table_name in TABLES:
        csv_path = os.path.join(CSV_DIR, f"{table_name}.csv")

        if not os.path.exists(csv_path):
            print(f"[!] {table_name}: CSV not found")
            continue

        try:
            # DuckDB can auto-detect schema from CSV
            con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}')")

            count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            print(f"[OK] {table_name:35} | {count:>10,} rows")
        except Exception as e:
            print(f"[ERROR] {table_name:35} | {str(e)[:50]}")

    print(f"\n[OK] Database setup complete: {DB_PATH}")
    con.close()

if __name__ == '__main__':
    setup()
