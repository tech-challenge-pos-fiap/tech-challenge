from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort
from app.domain.entities.product import Product


class UpdateProductUseCase:
    def __init__(self, repository_gateway: ProductRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, pk: int, product: Product) -> Product:
        return self.repository_gateway.update(pk, product)
