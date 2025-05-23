from app.application.ports.order_repository_port import OrderRepositoryPort
from app.domain.models.order import Order


class CreateOrderService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.repository = order_repository

    def execute(self, order_data: dict) -> Order:
        """Create a new order."""
        return self.repository.create(order_data)
