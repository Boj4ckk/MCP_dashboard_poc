from fastmcp.dependencies import Depends
from config.settings import settings
from data.repositories.sales_repo_interface import SalesRepositoryInterface
from services.sales.sales_services import SalesServices

# ____________ Sales ___________________________

def get_sales_repository() -> SalesRepositoryInterface:


    from infrastructure.duckdb_repo import DuckDBSalesRepository
    return DuckDBSalesRepository("C:\\Users\\BL211591\\Desktop\\MCP_dashboard_poc\\src\\data\\mock\\patissier.duckdb")


def get_sales_service(
        sales_repo = Depends(get_sales_repository)
) -> SalesServices:
    return SalesServices(sales_repo=sales_repo)