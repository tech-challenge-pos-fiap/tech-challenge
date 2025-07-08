from app.application.ports.product_repository_port import ProductRepositoryPort
from app.domain.entities.product import Product


class DeleteProductsService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.repository = product_repository

    def execute(self, id: int) -> bool:
        return self.repository.delete(id)
