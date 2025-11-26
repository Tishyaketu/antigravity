from dataclasses import dataclass

@dataclass(frozen=True)
class Product:
    """
    Immutable data structure representing a single product in the sales stream.
    Frozen to ensure data integrity during stream processing (functional style).
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
        # Calculated property to derive the absolute monetary value saved
        return self.actual_price - self.discounted_price