from abc import ABC, abstractmethod

from app.adapters.gateways.repositories.mappers.product_mapper import ProductMapper


class ProductRepositoryPort(ABC):
    @abstractmethod
    def save(self, product: ProductMapper) -> ProductMapper:
        pass

    @abstractmethod
    def list_by_category(self, category: str, skip: int = 0, limit: int = 10) -> list[ProductMapper]:
        """List products by category with pagination."""
        pass

    @abstractmethod
    def update(self, product_id: int, product: ProductMapper) -> ProductMapper:
        """Update an existing product."""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Delete a product by ID."""
        pass
