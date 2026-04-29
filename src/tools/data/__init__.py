from fastmcp import FastMCP
from .sales import sales_mcp
from .products import products_mcp
from .customers import customers_mcp
from .orders import orders_mcp
from .returns import returns_mcp
from .inventory import inventory_mcp
from .support import support_mcp
from .stores import stores_mcp
from .warehouses import warehouses_mcp

data_mcp = FastMCP("Data")

data_mcp.mount(sales_mcp)
data_mcp.mount(products_mcp)
data_mcp.mount(customers_mcp)
data_mcp.mount(orders_mcp)
data_mcp.mount(returns_mcp)
data_mcp.mount(inventory_mcp)
data_mcp.mount(support_mcp)
data_mcp.mount(stores_mcp)
data_mcp.mount(warehouses_mcp)
