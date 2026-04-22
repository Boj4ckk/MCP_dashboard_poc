
from prefab_ui import PrefabApp
from prefab_ui.components import Column, Heading
from fastmcp import FastMCP
from prefab_ui.components.charts import BarChart, ChartSeries
from fastapi.responses import HTMLResponse
from tools.data.sales import sales_mcp
mcp = FastMCP("Dashboard")


mcp.mount(sales_mcp)

if __name__ == "__main__":
    mcp.run()