from typing import Optional, List
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

support_mcp = FastMCP("Support")

@support_mcp.tool(description="Search and filter support tickets")
def get_support_tickets(
    customer_id: Optional[int] = None,
    store_id: Optional[int] = None,
    issue_type: Optional[str] = None,
    status: Optional[str] = None,
    escalation_flag: Optional[int] = None,
    min_resolution_time: Optional[float] = None,
    max_resolution_time: Optional[float] = None,
    joins: Optional[List[str]] = None,
    sort_by: Optional[str] = None,
    limit: Optional[int] = None,
    service = Depends(get_sales_service)
):
    """
    Search and filter support tickets with optional dimension joins
    - customer_id: filter by customer
    - store_id: filter by store
    - issue_type: filter by issue type (case-insensitive)
    - status: filter by status (case-insensitive)
    - escalation_flag: 0 or 1 escalation flag
    - min_resolution_time/max_resolution_time: resolution time range in hours
    - joins: list of dimension tables to join (dim_customer, dim_store, dim_date)
    - sort_by: any column name
    - limit: maximum number of results
    """
    return service.get_support_tickets(
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
