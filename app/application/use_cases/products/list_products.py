from typing import List

from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort
from app.domain.entities.product import Product


class ListProductsUseCase:
    def __init__(self, repository_gateway: ProductRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, category: str, skip: int = 0, limit: int = 10) -> List[Product]:
        return self.repository_gateway.list_by_category(category, skip, limit)
