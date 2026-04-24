#!/usr/bin/env python3
"""
Explore DuckDB tables and their schemas.
"""
import duckdb

def explore():
    conn = duckdb.connect("data/mock/patissier.duckdb")

    # Get all tables
    tables = conn.sql("SHOW TABLES").fetchall()

    print("\n" + "="*60)
    print("DUCKDB TABLES".center(60))
    print("="*60 + "\n")

    for table_name in tables:
        table = table_name[0]
        # Count rows
        count = conn.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"📊 {table:<35} | {count:>10,} rows")

        # Show schema
        schema = conn.sql(f"DESCRIBE {table}").fetchall()
        for col_name, col_type, *_ in schema:
            print(f"   ├─ {col_name:<30} {col_type}")
        print()

    conn.close()

if __name__ == '__main__':
    explore()
