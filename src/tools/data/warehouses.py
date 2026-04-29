from typing import Optional
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

warehouses_mcp = FastMCP("Warehouses")

@warehouses_mcp.tool(description="Search and filter warehouses")
def get_warehouses(
    warehouse_name: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    region: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter warehouses
    - warehouse_name: partial search (case-insensitive)
    - city: exact match
    - country: exact match
    - region: exact match
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_warehouses(
        warehouse_name=warehouse_name,
        city=city,
        country=country,
        region=region,
        sort_by=sort_by,
        limit=limit
    )
