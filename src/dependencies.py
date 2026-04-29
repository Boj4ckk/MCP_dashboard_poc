from fastmcp.dependencies import Depends
from config.settings import settings
from data.repositories.data_repo_interface import DataRepositoryInterface
from services.sales.sales_services import SalesServices

# ____________ Sales ___________________________

def get_data_repository() -> DataRepositoryInterface:
    from src.infrastructure.duckdb_repo import DuckDBRepository
    return DuckDBRepository("C:\\Users\\BL211591\\Desktop\\MCP_dashboard_poc\\src\\data\\mock\\patissier.duckdb")


def get_sales_service(
        data_repo = Depends(get_data_repository)
) -> SalesServices:
    return SalesServices(sales_repo=data_repo)