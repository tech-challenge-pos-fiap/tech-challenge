from app.adapters.gateways.repositories.mappers.product_mapper import ProductMapper
from app.adapters.gateways.repositories.product_repository_port import ProductRepositoryPort
from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort
from app.domain.entities.product import Product


class ProductRepositoryGateway(ProductRepositoryGatewayPort):
    def __init__(self, repository: ProductRepositoryPort):
        self.repository = repository

    def list_by_category(self, category, skip = 0, limit = 10) -> list[Product]:
        product_mappers = self.repository.list_by_category(category, skip, limit)
        return [product_mapper.to_entity() for product_mapper in product_mappers]

    def filter(self, **kwargs) -> list[Product]:
        product_mappers = self.repository.filter(**kwargs)
        return [product_mapper.to_entity() for product_mapper in product_mappers]

    def save(self, product: Product) -> Product:
        product_mapper = ProductMapper.from_entity(product)
        saved_product = self.repository.save(product_mapper)
        return saved_product.to_entity() if saved_product else None

    def update(self, product_id: int, product: Product) -> Product:
        product_mapper = ProductMapper.from_entity(product)
        updated_product = self.repository.update(product_id, product_mapper)
        return updated_product.to_entity() if updated_product else None

    def delete(self, product_id: int) -> bool:
        return self.repository.delete(product_id)
