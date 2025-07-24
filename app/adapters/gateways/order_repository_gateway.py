from app.adapters.gateways.repositories.mappers.order_mapper import OrderMapper
from app.adapters.gateways.repositories.order_repository_port import OrderRepositoryPort
from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.domain.entities.order import Order


class OrderRepositoryGateway(OrderRepositoryGatewayPort):
    def __init__(self, repository: OrderRepositoryPort):
        self.repository = repository

    def save(self, order: Order) -> Order:
        """Save a new order."""
        order_mapper = OrderMapper.from_entity(order)
        saved_order = self.repository.save(order_mapper)
        return saved_order.to_entity()

    def get(self, order_id) -> Order:
        """Get an order by ID."""
        order_mapper = self.repository.get(order_id)
        return order_mapper.to_entity() if order_mapper else None

    def update(self, order_id: str, order_data: Order) -> Order:
        """Update an existing order."""
        order_mapper = OrderMapper.from_entity(order_data)
        updated_order = self.repository.update(order_id, order_mapper)
        return updated_order.to_entity() if updated_order else None

    def get_all(self, skip: int = 0, limit: int = 10) -> list[Order]:
        """List orders with pagination."""
        order_mappers = self.repository.get_all(skip, limit)
        return [order_mapper.to_entity() for order_mapper in order_mappers]
