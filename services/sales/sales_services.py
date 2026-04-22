

from data.repositories.base import SalesRepositoryInterface
from services.sales.entities import ProductPerformance


class SalesServices:
    def __init__(self, sales_repo: SalesRepositoryInterface):
        self._sales_repo = sales_repo

    def get_product_performance(self,product_id:int, year:int) -> list[ProductPerformance]:
        return self._sales_repo.get_product_performance(
            product_id,year
        )

