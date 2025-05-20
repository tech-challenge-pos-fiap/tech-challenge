from abc import ABC, abstractmethod
from typing import List

from app.domain.models.product import Product


class ProductRepositoryPort(ABC):
    @abstractmethod
    def list_by_category(self, category: str, skip: int = 0, limit: int = 10) -> List[Product]:
        pass
