from typing import Optional, List
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

returns_mcp = FastMCP("Returns")

@returns_mcp.tool(description="Search and filter returns")
def get_returns(
    product_id: Optional[int] = None,
    customer_id: Optional[int] = None,
    order_id: Optional[str] = None,
    return_reason: Optional[str] = None,
    min_refund: Optional[float] = None,
    max_refund: Optional[float] = None,
    return_flag: Optional[int] = None,
    joins: Optional[List[str]] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter returns with optional dimension joins
    - product_id: filter by product
    - customer_id: filter by customer
    - order_id: filter by order
    - return_reason: filter by reason (case-insensitive)
    - min_refund/max_refund: refund amount range
    - return_flag: 0 or 1 return rate flag
    - joins: list of dimension tables to join (dim_product, dim_customer, dim_date)
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_returns(
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
