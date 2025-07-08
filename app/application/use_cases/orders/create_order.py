from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.domain.entities.order import Order


class CreateOrderUseCase:
    def __init__(self, repository_gateway: OrderRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, order_data: dict) -> Order:
        """Create a new order."""
        order = Order(**order_data)
        return self.repository_gateway.create(order)
