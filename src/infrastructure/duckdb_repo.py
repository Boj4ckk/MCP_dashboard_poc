import duckdb
from typing import Optional, List, Dict, Any
from data.repositories.data_repo_interface import DataRepositoryInterface

class DuckDBRepository(DataRepositoryInterface):
    def __init__(self, db_path: str):
        self.conn = duckdb.connect(db_path)
        self.table_schemas = self._load_schemas()
        self.table_joins = {
            "fact_sales": {"dim_product": "product_id", "dim_customer": "customer_id", "dim_store": "store_id", "dim_date": "date_id"},
            "fact_orders": {"dim_customer": "customer_id", "dim_store": "store_id", "dim_date": "date_id"},
            "fact_returns": {"dim_product": "product_id", "dim_customer": "customer_id", "dim_date": "date_id"},
            "fact_inventory_snapshot": {"dim_product": "product_id", "dim_warehouse": "warehouse_id", "dim_date": "date_id"},
            "fact_support_tickets": {"dim_customer": "customer_id", "dim_store": "store_id", "dim_date": "date_id"},
        }

    def _load_schemas(self) -> Dict[str, List[str]]:
        schemas = {}
        tables = ["dim_product", "dim_customer", "dim_store", "dim_warehouse", "dim_date", "dim_channel",
                  "fact_sales", "fact_orders", "fact_returns", "fact_inventory_snapshot", "fact_support_tickets"]
        for table in tables:
            result = self.conn.execute(f"PRAGMA table_info({table})").fetchall()
            schemas[table] = [row[1] for row in result]
        return schemas

    def get_data(
        self,
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        """Generic method to query any table with optional joins and filters"""
        if table not in self.table_schemas:
            raise ValueError(f"Table '{table}' not found")

        query = f"SELECT * FROM {table}"
        params = []

        # Build joins
        if joins and table in self.table_joins:
            for join_table in joins:
                if join_table in self.table_joins[table]:
                    fk = self.table_joins[table][join_table]
                    query += f" LEFT JOIN {join_table} ON {table}.{fk} = {join_table}.{fk}"

        # Build WHERE clause
        if filters:
            where_clauses = []
            for col, value in filters.items():
                if col not in self.table_schemas[table]:
                    continue
                if isinstance(value, str):
                    where_clauses.append(f"{table}.{col} ILIKE ?")
                    params.append(f"%{value}%")
                elif isinstance(value, tuple) and len(value) == 2:
                    if value[0] is not None:
                        where_clauses.append(f"{table}.{col} >= ?")
                        params.append(value[0])
                    if value[1] is not None:
                        where_clauses.append(f"{table}.{col} <= ?")
                        params.append(value[1])
                else:
                    where_clauses.append(f"{table}.{col} = ?")
                    params.append(value)

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

        # Order by
        if sort_by and sort_by in self.table_schemas[table]:
            query += f" ORDER BY {table}.{sort_by} ASC"

        # Limit
        if limit:
            query += " LIMIT ?"
            params.append(limit)

        rows = self.conn.execute(query, params).fetchall()

        # Get column names from result
        col_names = [desc[0] for desc in self.conn.description]

        return [dict(zip(col_names, row)) for row in rows]

    def get_products(
        self,
        name: Optional[str] = None,
        brand: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        status: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if name:
            filters["product_name"] = name
        if brand:
            filters["brand"] = brand
        if category:
            filters["category"] = category
        if subcategory:
            filters["subcategory"] = subcategory
        if min_price is not None or max_price is not None:
            filters["price"] = (min_price, max_price)
        if status:
            filters["lifecycle_status"] = status

        return self.get_data("dim_product", filters=filters, sort_by=sort_by, limit=limit)

    def get_customers(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        country: Optional[str] = None,
        city: Optional[str] = None,
        segment: Optional[str] = None,
        acquisition_channel: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if first_name:
            filters["first_name"] = first_name
        if last_name:
            filters["last_name"] = last_name
        if email:
            filters["email"] = email
        if country:
            filters["country"] = country
        if city:
            filters["city"] = city
        if segment:
            filters["segment"] = segment
        if acquisition_channel:
            filters["acquisition_channel"] = acquisition_channel

        return self.get_data("dim_customer", filters=filters, sort_by=sort_by, limit=limit)

    def get_sales(
        self,
        product_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        store_id: Optional[int] = None,
        order_id: Optional[str] = None,
        channel: Optional[str] = None,
        min_revenue: Optional[float] = None,
        max_revenue: Optional[float] = None,
        min_profit: Optional[float] = None,
        max_profit: Optional[float] = None,
        joins: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if product_id:
            filters["product_id"] = product_id
        if customer_id:
            filters["customer_id"] = customer_id
        if store_id:
            filters["store_id"] = store_id
        if order_id:
            filters["order_id"] = order_id
        if channel:
            filters["channel"] = channel
        if min_revenue is not None or max_revenue is not None:
            filters["revenue"] = (min_revenue, max_revenue)
        if min_profit is not None or max_profit is not None:
            filters["profit_amount"] = (min_profit, max_profit)

        return self.get_data("fact_sales", filters=filters, joins=joins, sort_by=sort_by, limit=limit)

    def get_orders(
        self,
        order_id: Optional[str] = None,
        customer_id: Optional[int] = None,
        store_id: Optional[int] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        order_status: Optional[int] = None,
        joins: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if order_id:
            filters["order_id"] = order_id
        if customer_id:
            filters["customer_id"] = customer_id
        if store_id:
            filters["store_id"] = store_id
        if min_value is not None or max_value is not None:
            filters["order_value"] = (min_value, max_value)
        if order_status is not None:
            filters["order_status_flag"] = order_status

        return self.get_data("fact_orders", filters=filters, joins=joins, sort_by=sort_by, limit=limit)

    def get_returns(
        self,
        product_id: Optional[int] = None,
        customer_id: Optional[int] = None,
        order_id: Optional[str] = None,
        return_reason: Optional[str] = None,
        min_refund: Optional[float] = None,
        max_refund: Optional[float] = None,
        return_flag: Optional[int] = None,
        joins: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if product_id:
            filters["product_id"] = product_id
        if customer_id:
            filters["customer_id"] = customer_id
        if order_id:
            filters["order_id"] = order_id
        if return_reason:
            filters["return_reason"] = return_reason
        if min_refund is not None or max_refund is not None:
            filters["refund_amount"] = (min_refund, max_refund)
        if return_flag is not None:
            filters["return_rate_flag"] = return_flag

        return self.get_data("fact_returns", filters=filters, joins=joins, sort_by=sort_by, limit=limit)

    def get_inventory(
        self,
        product_id: Optional[int] = None,
        warehouse_id: Optional[int] = None,
        min_stock: Optional[int] = None,
        max_stock: Optional[int] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        joins: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if product_id:
            filters["product_id"] = product_id
        if warehouse_id:
            filters["warehouse_id"] = warehouse_id
        if min_stock is not None or max_stock is not None:
            filters["stock_quantity"] = (min_stock, max_stock)
        if min_value is not None or max_value is not None:
            filters["stock_value"] = (min_value, max_value)

        return self.get_data("fact_inventory_snapshot", filters=filters, joins=joins, sort_by=sort_by, limit=limit)

    def get_support_tickets(
        self,
        customer_id: Optional[int] = None,
        store_id: Optional[int] = None,
        issue_type: Optional[str] = None,
        status: Optional[str] = None,
        escalation_flag: Optional[int] = None,
        min_resolution_time: Optional[float] = None,
        max_resolution_time: Optional[float] = None,
        joins: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if customer_id:
            filters["customer_id"] = customer_id
        if store_id:
            filters["store_id"] = store_id
        if issue_type:
            filters["issue_type"] = issue_type
        if status:
            filters["status"] = status
        if escalation_flag is not None:
            filters["escalation_flag"] = escalation_flag
        if min_resolution_time is not None or max_resolution_time is not None:
            filters["resolution_time_hours"] = (min_resolution_time, max_resolution_time)

        return self.get_data("fact_support_tickets", filters=filters, joins=joins, sort_by=sort_by, limit=limit)

    def get_stores(
        self,
        store_name: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        region: Optional[str] = None,
        store_type: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if store_name:
            filters["store_name"] = store_name
        if city:
            filters["city"] = city
        if country:
            filters["country"] = country
        if region:
            filters["region"] = region
        if store_type:
            filters["store_type"] = store_type

        return self.get_data("dim_store", filters=filters, sort_by=sort_by, limit=limit)

    def get_warehouses(
        self,
        warehouse_name: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        region: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        filters = {}
        if warehouse_name:
            filters["warehouse_name"] = warehouse_name
        if city:
            filters["city"] = city
        if country:
            filters["country"] = country
        if region:
            filters["region"] = region

        return self.get_data("dim_warehouse", filters=filters, sort_by=sort_by, limit=limit)