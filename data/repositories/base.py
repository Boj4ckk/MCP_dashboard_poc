from abc import ABC, abstractmethod


class SalesRepositoryInterface(ABC):

    @abstractmethod
    def get_product_performance(
        self,
        product_id:int,
        year:int
    ) -> list[dict]:
        ...

