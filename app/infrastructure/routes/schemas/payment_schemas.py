from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field


class Identification(BaseModel):
    type: Optional[str] = Field(None, description="Tipo de identificação (CPF, CNPJ)")
    number: Optional[str] = Field(
        None,
        pattern=r"^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$",
        description="Número do documento (somente CPF, com ou sem pontuação)",
    )


class Payer(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Email do pagador")
    identification: Optional[Identification] = Field(None, description="Identificação do pagador")


class ProcessPaymentRequest(BaseModel):
    transaction_amount: Decimal = Field(..., gt=0, description="Valor da transação (deve ser maior que zero)")
    description: Optional[str] = Field(None, min_length=1, max_length=256, description="Descrição do pagamento")
    order_id: Optional[int] = Field(None, description="ID da ordem associada ao pagamento")
    payer: Optional[Payer] = Field(None, description="Informações do pagador")

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_amount": 100,
                "description": "Título do produto",
                "order_id": 1,
                "payer": {"email": "teste@email.com", "identification": {"type": "CPF", "number": "191.191.191-00"}},
            }
        }


class PaymentResponse(BaseModel):
    id: int = Field(..., description="ID do pagamento")
    status: str = Field(..., description="Status do pagamento")
    transaction_amount: float = Field(..., description="Valor da transação")
    payment_method: str = Field(..., description="ID do método de pagamento")
    order_id: int = Field(None, description="ID da ordem associada ao pagamento")
    paid_at: Optional[datetime] = None
    mp_payment_id: Optional[str] = Field(None, description="Mercado Pago payment ID")

    class Config:
        from_attributes = True


class WebhookData(BaseModel):
    """Schema for Mercado Pago webhook data"""

    id: str = Field(..., description="Mercado Pago payment ID")
    status: str = Field(..., description="Payment status from Mercado Pago")
    status_detail: Optional[str] = Field(None, description="Status detail from Mercado Pago")
    transaction_amount: Optional[float] = Field(None, description="Transaction amount")
    payment_method: Optional[Dict[str, Any]] = Field(None, description="Payment method information")
    external_reference: Optional[str] = Field(None, description="External reference (order ID)")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123456789",
                "status": "approved",
                "status_detail": "accredited",
                "transaction_amount": 100.00,
                "payment_method": {"type": "credit_card"},
                "external_reference": "order_123",
            }
        }


class WebhookResponse(BaseModel):
    message: str = Field(..., description="Response message from webhook processing")
