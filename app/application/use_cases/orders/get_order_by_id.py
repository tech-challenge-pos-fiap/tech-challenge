from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.domain.entities.order import Order


class GetOrderUseCase:
    def __init__(self, repository_gateway: OrderRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, order_id: int) -> Order:
        """Get all orders."""
        return self.repository_gateway.get(order_id)
