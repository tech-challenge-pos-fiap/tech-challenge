from app.application.ports.order_repository_port import OrderRepositoryPort
from app.domain.models.order import Order


class GetOrderService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.repository = order_repository

    def execute(self, order_id: int) -> Order:
        """Get all orders."""
        return self.repository.get(order_id)
