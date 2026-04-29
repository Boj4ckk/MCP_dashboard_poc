from typing import Optional
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

products_mcp = FastMCP("Products")

@products_mcp.tool(description="Search and filter products by various criteria")
def get_products(
    name: Optional[str] = None,
    brand: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter products by various criteria
    - name: partial product name search (case-insensitive)
    - brand: filter by brand (case-insensitive)
    - category: exact category match
    - subcategory: exact subcategory match
    - min_price/max_price: price range filtering
    - status: 'active' or 'discontinued'
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_products(
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
