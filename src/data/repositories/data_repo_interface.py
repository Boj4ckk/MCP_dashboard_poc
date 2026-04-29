from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class DataRepositoryInterface(ABC):

    @abstractmethod
    def get_data(
        self,
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        joins: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def get_warehouses(
        self,
        warehouse_name: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        region: Optional[str] = None,
        sort_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[dict]:
        ...

