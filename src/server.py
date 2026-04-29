from fastmcp import FastMCP
from fastapi.responses import HTMLResponse
from src.tools.data import data_mcp
from src.tools.ui.charts import charts_mcp

mcp = FastMCP("dashboard")

mcp.mount(data_mcp)
mcp.mount(charts_mcp)

if __name__ == "__main__":
    mcp.run()