from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    """
    Immutable representation of a Product.
    Attributes match the business domain.
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
        """
        Calculates the absolute money saved.
        Logic: Actual Price - Discounted Price
        """
        return self.actual_price - self.discounted_price