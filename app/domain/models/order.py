from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class OrderStatus(str, Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


@dataclass
class Order:
    id: Optional[int]
    products: list
    customer_id: Optional[int]
    status: OrderStatus
    total_price: Decimal
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
