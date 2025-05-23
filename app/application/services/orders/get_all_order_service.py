from app.application.ports.order_repository_port import OrderRepositoryPort
from app.domain.models.order import Order


class GetAllOrderService:
    def __init__(self, order_repository: OrderRepositoryPort):
        self.repository = order_repository

    def execute(self, skip: int = 0, limit: int = 10) -> list[Order]:
        """Get all orders."""
        return self.repository.get_all(skip, limit)
