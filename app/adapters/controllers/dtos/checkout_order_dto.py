from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class ProductOrderDTO(BaseModel):
    product_id: int
    quantity: int

class CheckoutOrderDTO(BaseModel):
    products: list[ProductOrderDTO] = Field(..., description="Lista de produtos")

class CheckoutOrderResponseDTO(BaseModel):
    order_id: int
    total_price: Decimal
