
# infrastructure/duckdb_sales_repo.py — couche externe, implémente le contrat

import duckdb
from data.repositories.sales_repo_interface import SalesRepositoryInterface
from services.sales.entities import ProductPerformance

class DuckDBSalesRepository(SalesRepositoryInterface):

    def __init__(self, db_path: str):
        self.conn = duckdb.connect(db_path)

    def get_product_by_aliase_name(self,name:str):
        row = self.conn.execute("""
            SELECT
                product_id,
                product_name
            FROM dim_product
            WHERE product_name = ?
        """, [name]).fetchone()
        if row:
            return {"product_id": row[0], "product_name": row[1]}
        else:
            return None