from typing import Optional
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

stores_mcp = FastMCP("Stores")

@stores_mcp.tool(description="Search and filter stores")
def get_stores(
    store_name: Optional[str] = None,
    city: Optional[str] = None,
    country: Optional[str] = None,
    region: Optional[str] = None,
    store_type: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter stores
    - store_name: partial search (case-insensitive)
    - city: exact match
    - country: exact match
    - region: exact match
    - store_type: filter by type (e.g., 'flagship')
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_stores(
        store_name=store_name,
        city=city,
        country=country,
        region=region,
        store_type=store_type,
        sort_by=sort_by,
        limit=limit
    )
