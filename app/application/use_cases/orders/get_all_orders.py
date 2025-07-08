from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.domain.entities.order import Order


class GetAllOrderUseCase:
    def __init__(self, repository_gateway: OrderRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, skip: int = 0, limit: int = 10) -> list[Order]:
        """Get all orders."""
        return self.repository_gateway.get_all(skip, limit)
