from abc import ABC, abstractmethod


class SalesRepositoryInterface(ABC):

    @abstractmethod
    def get_product_by_aliase_name(self,name:str) -> dict:
        ...

