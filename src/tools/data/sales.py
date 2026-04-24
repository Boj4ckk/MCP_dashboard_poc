from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, Heading
from prefab_ui.components.charts import BarChart, ChartSeries
from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_sales_service

sales_mcp = FastMCP("Sales")

@sales_mcp.tool(description="Get product details by aliase name")
def get_product_by_aliase_name(
    name: str,
    service = Depends(get_sales_service)
) :
    return service.get_product_by_aliase_name(name)
    
    
  