from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    """
    Immutable representation of a Product.
    """
    name: str
    category: str
    discounted_price: float
    actual_price: float
    discount_percentage: float
    rating: float
    rating_count: int

    @property
    def savings(self) -> float:
        return self.actual_price - self.discounted_price