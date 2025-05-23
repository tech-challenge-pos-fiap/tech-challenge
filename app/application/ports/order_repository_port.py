from abc import ABC, abstractmethod


class OrderRepositoryPort(ABC):
    @abstractmethod
    def create(self, order_data):
        """Create a new order."""
        pass
    @abstractmethod
    def get(self, order_id):
        """Get an order by ID."""
        pass
    @abstractmethod
    def update(self, order_id, order_data):
        """Update an existing order."""
        pass
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10):
        """List orders with pagination."""
        pass
