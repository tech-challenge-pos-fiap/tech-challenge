from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class OrderDTO(BaseModel):
    id: Optional[int] = Field(None, description="ID do pedido")
    products: list = Field(..., description="Lista de produtos no pedido")
    status: str = Field(..., description="Status do pedido")
    total_price: Optional[Decimal] = Field(None, description="Preço total do pedido")
    customer_id: Optional[int] = Field(None, description="ID do cliente associado ao pedido")
    created_at: Optional[str] = Field(None, description="Data de criação do pedido")
    updated_at: Optional[str] = Field(None, description="Data da última atualização do pedido")
