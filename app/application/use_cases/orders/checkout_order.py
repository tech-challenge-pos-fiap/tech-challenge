from app.adapters.gateways.order_repository_gateway import OrderRepositoryGateway

from app.domain.entities.order import Order, OrderStatus

class CheckoutOrder:
    def __init__(self, repository: OrderRepositoryGateway):
        self.repository = repository

    def execute(self, order_data: dict) -> dict:
        order_data["status"] = OrderStatus.RECEIVED
        order = self.repository.create(order_data)
        return {
            "order_id": order.id,
            "total_price": order.total_price
        }
