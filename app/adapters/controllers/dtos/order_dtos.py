from enum import Enum

from pydantic import BaseModel


class OrderStatus(str, Enum):
    PENDING = 'pending'
    RECEIVED = 'received'
    IN_PREPARATION = 'in_preparation'
    READY = 'ready'
    FINISHED = 'finished'


class UpdateOrderStatusDTO(BaseModel):
    status: OrderStatus
