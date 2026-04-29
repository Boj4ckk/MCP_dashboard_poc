from typing import Optional, List
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from src.dependencies import get_sales_service

sales_mcp = FastMCP("Sales")

@sales_mcp.tool(description="Search and filter sales transactions")
def get_sales(
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
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """Search and filter sales transactions with optional dimension joins"""
    return service.get_sales(
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
