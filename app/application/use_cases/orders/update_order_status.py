from app.adapters.gateways.order_repository_gateway import OrderRepositoryGateway
from app.domain.entities.order import Order, OrderStatus


class UpdateOrderStatus:
    def __init__(self, repository: OrderRepositoryGateway):
        self.repository = repository

    def execute(self, order_id: int, status: str) -> Order:
        if status not in [
            OrderStatus.RECEIVED,
            OrderStatus.IN_PREPARATION,
            OrderStatus.READY,
            OrderStatus.FINISHED,
        ]:
            raise ValueError("Status inválido.")
        return self.repository.update(order_id, {"status": status})
