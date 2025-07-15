from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort
from app.domain.entities.product import Product


class CreateProductUseCase:
    def __init__(self, repository_gateway: ProductRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, product_data) -> Product:
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category,
            image_path=product_data.image_path,
        )
        return self.repository_gateway.save(product)
