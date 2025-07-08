from app.application.ports.product_repository_port import ProductRepositoryPort
from app.domain.entities.product import Product


class UpdateProductsService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.repository = product_repository

    def execute(self, id: int, product: Product) -> Product:
        return self.repository.update(id, product)
