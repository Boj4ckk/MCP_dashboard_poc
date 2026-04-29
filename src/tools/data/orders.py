from typing import Optional, List
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

orders_mcp = FastMCP("Orders")

@orders_mcp.tool(description="Search and filter orders")
def get_orders(
    order_id: Optional[str] = None,
    customer_id: Optional[int] = None,
    store_id: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    order_status: Optional[int] = None,
    joins: Optional[List[str]] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter orders with optional dimension joins
    - order_id: specific order ID
    - customer_id: filter by customer
    - store_id: filter by store
    - min_value/max_value: order value range
    - order_status: 0 or 1 status flag
    - joins: list of dimension tables to join (dim_customer, dim_store, dim_date)
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_orders(
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
