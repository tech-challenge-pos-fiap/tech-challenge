from pydantic import BaseModel

from app.domain.entities.order import OrderStatus


class GetAllOrdersRequestSchema(BaseModel):
    skip: int = 0
    limit: int = 10


class CreateOrderRequestSchema(BaseModel):
    products: list
    customer_id: int

    class Config:
        orm_mode = True


class OrderResponseSchema(BaseModel):
    id: int
    products: list
    customer_id: int
    status: OrderStatus
    total_price: float
