from app.adapters.gateways.order_repository_gateway import OrderRepositoryGateway
from app.domain.entities.order import Order


class UpdateOrderStatusUseCase:
    def __init__(self, repository: OrderRepositoryGateway):
        self.repository = repository

    def execute(self, order_id: int, new_status: str) -> Order:
        order = self.repository.get(order_id)
        order.update_status(new_status)
        return self.repository.update(order_id, order)
