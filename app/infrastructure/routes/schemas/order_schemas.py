from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from app.infrastructure.routes.schemas.customer_schemas import CustomerResponseSchema
from app.infrastructure.routes.schemas.product_schemas import ProductResponseSchema


class OrderItemSchema(BaseModel):
    product: ProductResponseSchema = Field(..., description="Produto no pedido")
    quantity: int


class OrderSchema(BaseModel):
    id: Optional[int] = Field(None, description="ID do pedido")
    items: list[OrderItemSchema] = Field(..., description="Lista de produtos no pedido")
    status: Optional[str] = Field(None, description="Status do pedido")
    total_price: Optional[Decimal] = Field(None, description="Preço total do pedido")
    customer: Optional[CustomerResponseSchema] = Field(None, description="Cliente associado ao pedido")

    class Config:
        from__attributes = True


class CreateOrderItemRequestSchema(BaseModel):
    product_id: int = Field(..., description="ID do produto")
    quantity: int


class CreateOrderRequestSchema(BaseModel):
    items: list[CreateOrderItemRequestSchema] = Field(..., description="Lista de produtos no pedido")
    customer_id: Optional[int] = Field(None, description="ID do cliente associado ao pedido")
