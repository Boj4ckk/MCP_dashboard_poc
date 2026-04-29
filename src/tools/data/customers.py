from typing import Optional
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

customers_mcp = FastMCP("Customers")

@customers_mcp.tool(description="Search and filter customers by various criteria")
def get_customers(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[str] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    segment: Optional[str] = None,
    acquisition_channel: Optional[str] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter customers by various criteria
    - first_name: partial search (case-insensitive)
    - last_name: partial search (case-insensitive)
    - email: partial search (case-insensitive)
    - country: exact match
    - city: exact match
    - segment: customer segment filter
    - acquisition_channel: how customer was acquired
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_customers(
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
