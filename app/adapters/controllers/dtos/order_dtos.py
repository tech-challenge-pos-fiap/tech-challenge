from enum import Enum
from pydantic import BaseModel, Field

class OrderStatus(str, Enum):
    RECEIVED = 'received'
    IN_PREPARATION = 'in_preparation'
    READY = 'ready'
    FINISHED = 'finished'

class UpdateOrderStatusDTO(BaseModel):
    status: OrderStatus

class CheckoutOrderDTO(BaseModel):
    products: list[ProductOrderDTO]
    customer_id: Optional[int] = None
    total_price: float = Field(..., gt=0, description="Total price of the order")