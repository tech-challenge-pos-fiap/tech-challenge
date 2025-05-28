from app.application.ports.order_repository_port import OrderRepositoryPort
from app.domain.models.order import Order


class UpdateOrderService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.repository = order_repository

    def execute(self, order_id: int, order_data: dict) -> Order:
        """Update a new order."""
        return self.repository.update(order_id, order_data)
