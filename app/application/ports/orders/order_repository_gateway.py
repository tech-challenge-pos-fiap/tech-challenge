from abc import ABC, abstractmethod

from app.domain.entities.order import Order


class OrderRepositoryGatewayPort(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        """Save a new order."""
        pass

    @abstractmethod
    def get(self, order_id) -> Order:
        """Get an order by ID."""
        pass

    @abstractmethod
    def update(self, order_id, order_data) -> Order:
        """Update an existing order."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> list[Order]:
        """List orders with pagination."""
        pass
