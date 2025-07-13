from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.domain.entities.order import Order, OrderStatus


@dataclass
class OrderMapper:
    id: int
    products: list
    customer_id: Optional[int]
    status: OrderStatus
    total_price: Decimal
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @classmethod
    def from_entity(cls, order: Order) -> 'OrderMapper':
        return cls(
            id=order.id,
            products=order.products,
            customer_id=order.customer_id,
            status=order.status,
            total_price=order.total_price,
            created_at=order.created_at,
            updated_at=order.updated_at
        )

    def to_entity(self) -> Order:
        return Order(
            id=self.id,
            products=self.products,
            customer_id=self.customer_id,
            status=self.status,
            total_price=self.total_price,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
