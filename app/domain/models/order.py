from enum import Enum
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


class OrderStatus(str, Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


@dataclass
class Order:
    id: Optional[int]
    products: list
    status: OrderStatus
    total_price: Decimal
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
