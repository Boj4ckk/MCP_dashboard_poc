
# infrastructure/duckdb_sales_repo.py — couche externe, implémente le contrat

import duckdb
from data.repositories.base import SalesRepositoryInterface
from services.sales.entities import ProductPerformance

class DuckDBSalesRepository(SalesRepositoryInterface):

    def __init__(self, db_path: str):
        self.conn = duckdb.connect(db_path)

    def get_product_performance(
        self,
        product_id: int,
        year: int
    ) -> list[ProductPerformance]:
        rows = self.conn.execute("""
            SELECT
                d.month                  as month,
                p.name                   as product_name,
                SUM(s.revenue)           as revenue,
                SUM(s.quantity)          as units_sold,
                SUM(s.profit_amount)     as profit
            FROM sales s
            JOIN dim_date  d ON s.date_id    = d.date_id
            JOIN products  p ON s.product_id = p.product_id
            WHERE s.product_id = ?
            AND d.year        = ?
            GROUP BY d.month, p.name
            ORDER BY d.month
        """, [product_id, year]).fetchall()

        return [
            ProductPerformance(
                month=r[0],
                product_name=r[1],
                revenue=r[2],
                units_sold=r[3],
                profit=r[4]
            )
            for r in rows
        ]