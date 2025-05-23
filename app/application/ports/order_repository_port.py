from abc import ABC, abstractmethod

from app.domain.models.order import Order


class OrderRepositoryPort(ABC):
    @abstractmethod
    def create(self, order_data) -> Order:
        """Create a new order."""
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
