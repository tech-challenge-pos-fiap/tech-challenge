from app.application.ports.product_repository_port import ProductRepositoryPort
from app.domain.models.product import Product


class CreateProductsService:
    def __init__(self, product_repository: ProductRepositoryPort):
        self.repository = product_repository

    def execute(self, product: Product) -> Product:
        return self.repository.save(product)
