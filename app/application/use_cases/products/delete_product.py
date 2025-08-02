from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort


class DeleteProductUseCase:
    def __init__(self, repository_gateway: ProductRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, pk: int) -> bool:
        return self.repository_gateway.delete(pk)
