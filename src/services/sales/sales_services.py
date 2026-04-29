from typing import Optional, List
from data.repositories.data_repo_interface import DataRepositoryInterface


class SalesServices:
    def __init__(self, sales_repo: DataRepositoryInterface):
        self._sales_repo = sales_repo

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
        return self._sales_repo.get_products(
            name=name,
            brand=brand,
            category=category,
            subcategory=subcategory,
            min_price=min_price,
            max_price=max_price,
            status=status,
            sort_by=sort_by,
            limit=limit
        )

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
        return self._sales_repo.get_customers(
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            city=city,
            segment=segment,
            acquisition_channel=acquisition_channel,
            sort_by=sort_by,
            limit=limit
        )

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
        return self._sales_repo.get_sales(
            product_id=product_id,
            customer_id=customer_id,
            store_id=store_id,
            order_id=order_id,
            channel=channel,
            min_revenue=min_revenue,
            max_revenue=max_revenue,
            min_profit=min_profit,
            max_profit=max_profit,
            joins=joins,
            sort_by=sort_by,
            limit=limit
        )

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
        return self._sales_repo.get_orders(
            order_id=order_id,
            customer_id=customer_id,
            store_id=store_id,
            min_value=min_value,
            max_value=max_value,
            order_status=order_status,
            joins=joins,
            sort_by=sort_by,
            limit=limit
        )

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
        return self._sales_repo.get_returns(
            product_id=product_id,
            customer_id=customer_id,
            order_id=order_id,
            return_reason=return_reason,
            min_refund=min_refund,
            max_refund=max_refund,
            return_flag=return_flag,
            joins=joins,
            sort_by=sort_by,
            limit=limit
        )

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
        return self._sales_repo.get_inventory(
            product_id=product_id,
            warehouse_id=warehouse_id,
            min_stock=min_stock,
            max_stock=max_stock,
            min_value=min_value,
            max_value=max_value,
            joins=joins,
            sort_by=sort_by,
            limit=limit
        )

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
        return self._sales_repo.get_support_tickets(
            customer_id=customer_id,
            store_id=store_id,
            issue_type=issue_type,
            status=status,
            escalation_flag=escalation_flag,
            min_resolution_time=min_resolution_time,
            max_resolution_time=max_resolution_time,
            joins=joins,
            sort_by=sort_by,
            limit=limit
        )

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
        return self._sales_repo.get_stores(
            store_name=store_name,
            city=city,
            country=country,
            region=region,
            store_type=store_type,
            sort_by=sort_by,
            limit=limit
        )

    def get_warehouses(
        self,
        warehouse_name: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        region: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        return self._sales_repo.get_warehouses(
            warehouse_name=warehouse_name,
            city=city,
            country=country,
            region=region,
            sort_by=sort_by,
            limit=limit
        )
