from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort
from app.domain.entities.product import Product


class CreateProductUseCase:
    def __init__(self, repository_gateway: ProductRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, product_data: dict) -> Product:
        product = Product(
            name=product_data.get("name"),
            description=product_data.get("description"),
            price=product_data.get("price"),
            category=product_data.get("category"),
            image_path=product_data.get("image_path"),
        )
        return self.repository_gateway.save(product)
