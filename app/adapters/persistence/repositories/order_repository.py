from sqlalchemy.orm import Session

from app.adapters.persistence.models.order import OrderModel
from app.application.ports.order_repository_port import OrderRepositoryPort
from app.domain.models.order import Order

class OrderRepository(OrderRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_data: dict) -> Order:
        """Create a new order."""
        print(order_data, flush=True)
        order = OrderModel(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return Order(order.id, order.customer_id, order.total_amount, order.status)

    def get(self, order_id: int) -> Order:
        """Get an order by ID."""
        order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if order:
            return Order(order.id, order.customer_id, order.total_amount, order.status)
        return None

    def update(self, order_id: int, order_data: dict) -> Order:
        """Update an existing order."""
        order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if order:
            for key, value in order_data.items():
                setattr(order, key, value)
            self.db.commit()
            self.db.refresh(order)
            return Order(order.id, order.customer_id, order.total_amount, order.status)
        return None

    def get_all(self, skip: int = 0, limit: int = 10) -> list[Order]:
        """List orders with pagination."""
        results = self.db.query(OrderModel).offset(skip).limit(limit).all()
        return [Order(order.id, order.customer_id, order.total_amount, order.status) for order in results]
