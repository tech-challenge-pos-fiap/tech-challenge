from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort
from app.domain.entities.product import Product


class CreateProductUseCase:
    def __init__(self, repository_gateway: ProductRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, product_data: dict) -> Product:
        product = Product(**product_data)
        return self.repository_gateway.save(product)
