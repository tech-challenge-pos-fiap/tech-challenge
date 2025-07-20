from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional

from app.domain.entities.customer import Customer
from app.domain.entities.product import Product


class OrderStatus(str, Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


@dataclass
class OrderItem:
    product: Product
    quantity: int


@dataclass
class Order:
    items: list[OrderItem]
    customer: Optional[Customer] = None
    total_price: Decimal = field(default=Decimal('0.00'))
    status: OrderStatus = field(default=OrderStatus.PENDING)
    id: Optional[int] = field(default=None)

    @classmethod
    def create(cls, items: list[OrderItem], customer: Optional[Customer] = None) -> 'Order':
        if not items:
            raise ValueError("Order must have at least one item.")
        total_price = sum(item.quantity * item.product.price for item in items)

        return cls(
            items=items,
            customer=customer,
            total_price=total_price,
        )
