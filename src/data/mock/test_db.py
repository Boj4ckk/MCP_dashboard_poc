#!/usr/bin/env python3
"""
Test DuckDB Patissier database - Basic query per table.
"""
import duckdb

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

def test_tables():
    try:
        con = duckdb.connect(DB_PATH, read_only=True)
        print(f"[OK] Connected to {DB_PATH}\n")
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return

    for table in TABLES:
        try:
            result = con.execute(f"SELECT COUNT(*) as row_count FROM {table}").fetchall()
            count = result[0][0]

            # Get first row sample
            sample = con.execute(f"SELECT * FROM {table} LIMIT 1").fetchall()

            print(sample)
            if sample:
                print(f"     Sample: {str(sample[0][:3])[:60]}...")
        except Exception as e:
            print(f"[ERROR] {table:35} | {str(e)[:50]}")

    con.close()
    print(f"\n[OK] All tests completed.")

if __name__ == '__main__':
    test_tables()
