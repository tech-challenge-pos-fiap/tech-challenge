from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.product import Product


class ProductRepositoryGatewayPort(ABC):
    @abstractmethod
    def list_by_category(self, category: str, skip: int = 0, limit: int = 10) -> List[Product]:
        """Return a customer by category"""
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Persist a product and return it (possibly with ID populated)."""
        pass

    @abstractmethod
    def update(self, product_id: int, product: Product) -> Product:
        """Update a product based on a id passed"""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """Delete a product based on a id passed"""
        pass
