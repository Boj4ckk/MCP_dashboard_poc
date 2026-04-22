



from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service
from services.sales.sales_services import SalesServices


sales_mcp = FastMCP("Sales")
@sales_mcp.tool(app=True)
def get_product_performance(
    product_id:int,
    year:int,
    service = Depends(get_sales_service)
    
) -> list[dict]:
    results = service.get_product_performance(product_id,year)
    return [vars(r) for r in results]

    