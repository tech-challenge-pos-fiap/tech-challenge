from typing import List

from app.application.ports.product_repository_port import ProductRepositoryPort
from app.domain.models.product import Product


class ListProductsService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.repository = product_repository

    def execute(self, category: str, skip: int = 0, limit: int = 10) -> List[Product]:
        return self.repository.list_by_category(category, skip, limit)
