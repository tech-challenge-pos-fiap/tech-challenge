from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.domain.entities.order import Order


class UpdateOrderService:
    def __init__(self, repository_gateway: OrderRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, order_id: int, order_data: dict) -> Order:
        """Update a new order."""
        return self.repository_gateway.update(order_id, order_data)
