

from data.repositories.sales_repo_interface import SalesRepositoryInterface
from services.sales.entities import ProductPerformance


class SalesServices:
    def __init__(self, sales_repo: SalesRepositoryInterface):
        self._sales_repo = sales_repo

    def get_product_by_aliase_name(self,name:str):
        return self._sales_repo.get_product_by_aliase_name(name)

