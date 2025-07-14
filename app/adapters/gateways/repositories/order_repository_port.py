from abc import ABC, abstractmethod

from app.adapters.gateways.mappers.order_mapper import OrderMapper


class OrderRepositoryPort(ABC):
    @abstractmethod
    def save(self, order: OrderMapper) -> OrderMapper:
        pass

    @abstractmethod
    def get(self, order_id: str) -> OrderMapper:
        """Return an order by ID or None if not found."""
        pass

    @abstractmethod
    def update(self, order_id: str, order_data: OrderMapper) -> OrderMapper:
        """Update an existing order."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> list[OrderMapper]:
        """List orders with pagination."""
        pass
