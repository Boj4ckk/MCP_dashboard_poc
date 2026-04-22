from fastmcp.dependencies import Depends
from config.settings import Settings
from data.repositories.base import SalesRepositoryInterface
from services.sales.sales_services import SalesServices

# ____________ Sales ___________________________

def get_sales_repository() -> SalesRepositoryInterface:
  
  
    from infrastructure.duckdb_repo import DuckDBSalesRepository
    return DuckDBSalesRepository(Settings.DUCK_PATH)


def get_sales_service(
        sales_repo = Depends(get_sales_repository)
) -> SalesServices:
    return SalesServices(sales_repo=sales_repo)