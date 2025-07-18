from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from .product_dtos import ProductOrderDTO

class OrderStatus(str, Enum):
    RECEIVED = 'received'
    IN_PREPARATION = 'in_preparation'
    READY = 'ready'
    FINISHED = 'finished'

class UpdateOrderStatusDTO(BaseModel):
    status: OrderStatus

class CheckoutOrderDTO(BaseModel):
    products: list[ProductOrderDTO]
    customer_id: Optional[int] = None = Field(
        None, description="ID of the customer placing the order"
    )
    total_price: float = Field(..., gt=0, description="Total price of the order")