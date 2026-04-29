from typing import Optional, List
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

inventory_mcp = FastMCP("Inventory")

@inventory_mcp.tool(description="Search and filter inventory snapshots")
def get_inventory(
    product_id: Optional[int] = None,
    warehouse_id: Optional[int] = None,
    min_stock: Optional[int] = None,
    max_stock: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    joins: Optional[List[str]] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter inventory snapshots with optional dimension joins
    - product_id: filter by product
    - warehouse_id: filter by warehouse
    - min_stock/max_stock: stock quantity range
    - min_value/max_value: stock value range
    - joins: list of dimension tables to join (dim_product, dim_warehouse, dim_date)
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_inventory(
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
