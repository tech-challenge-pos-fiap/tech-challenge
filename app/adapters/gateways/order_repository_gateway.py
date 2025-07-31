from app.adapters.gateways.repositories.mappers.order_mapper import OrderMapper
from app.adapters.gateways.repositories.order_repository_port import OrderRepositoryPort
from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.application.use_cases.orders.update_order_status import UpdateOrderStatus
from app.domain.entities.order import Order


class OrderRepositoryGateway(OrderRepositoryGatewayPort):
    def __init__(self, repository: OrderRepositoryPort):
        self.repository = repository

    def save(self, order: Order) -> Order:
        order_mapper = OrderMapper.from_entity(order)
        saved_order = self.repository.save(order_mapper)
        return saved_order.to_entity()

    def get(self, order_id: str) -> Order:
        order_mapper = self.repository.get(order_id)
        return order_mapper.to_entity() if order_mapper else None

    def update(self, order_id: str, order_data: Order) -> Order:
        order_mapper = OrderMapper.from_entity(order_data)
        updated_order = self.repository.update(order_id, order_mapper)
        return updated_order.to_entity() if updated_order else None

    def delete(self, order_id: str) -> None:
        self.repository.delete(order_id)

    def get_all(self, skip: int = 0, limit: int = 10) -> list[Order]:
        order_mappers = self.repository.get_all(skip, limit)
        return [order_mapper.to_entity() for order_mapper in order_mappers]

    def update_status(self, order_id: str, status: str) -> Order:
        updated_order = self.repository.update_status(order_id, status)
        return updated_order.to_entity() if updated_order else None

    def checkout(self, order_id: str) -> Order:
        checked_out_order = self.repository.checkout(order_id)
        return checked_out_order.to_entity() if checked_out_order else None

    def get_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 10) -> list[Order]:
        order_mappers = self.repository.get_by_customer_id(customer_id, skip, limit)
        return [mapper.to_entity() for mapper in order_mappers]

    def get_by_status(self, status: str, skip: int = 0, limit: int = 10) -> list[Order]:
        order_mappers = self.repository.get_by_status(status, skip, limit)
        return [mapper.to_entity() for mapper in order_mappers]

    def count_orders(self) -> int:
        return self.repository.count_orders()

    def exists(self, order_id: str) -> bool:
        return self.repository.exists(order_id)