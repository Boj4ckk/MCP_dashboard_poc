from dataclasses import dataclass

@dataclass
class ProductPerformance:
    month: str
    product_name:str
    revenue: float
    units_sold: int
    profit: int = 0
