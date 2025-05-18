from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional
from decimal import Decimal

class IdentificationDTO(BaseModel):
    type: Optional[str] = Field(None, description="Tipo de identificação (CPF, CNPJ)")
    number: Optional[str] = Field(
        None,
        pattern=r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$',
        description="Número do documento (somente CPF, com ou sem pontuação)"
    )

class PayerDTO(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Email do pagador")
    identification: Optional[IdentificationDTO] = Field(None, description="Identificação do pagador")

class CreatePixPaymentRequestDTO(BaseModel):
    transaction_amount: Decimal = Field(
        ..., 
        gt=0,
        description="Valor da transação (deve ser maior que zero)"
    )
    description: Optional[str] = Field(
        None, 
        min_length=1,
        max_length=256,
        description="Descrição do pagamento"
    )
    payer: Optional[PayerDTO] = Field(None, description="Informações do pagador")

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_amount": 100,
                "description": "Título do produto",
                "payer": {
                    "email": "teste@email.com",
                    "identification": {
                        "type": "CPF",
                        "number": "191.191.191-00"
                    }
                }
            }
        }

class PixPaymentResponseDTO(BaseModel):
    id: str = Field(..., description="ID do pagamento")
    status: str = Field(..., description="Status do pagamento")
    qr_code: str = Field(..., description="Código QR do PIX")
    qr_code_base64: str = Field(..., description="Código QR em base64")
    transaction_amount: Decimal = Field(..., description="Valor da transação")
    created_at: str = Field(..., description="Data de criação do pagamento")
    updated_at: str = Field(..., description="Data da última atualização")
    payer: PayerDTO = Field(..., description="Informações do pagador")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123456789",
                "status": "pending",
                "qr_code": "00020101021226870014br.gov.bcb.pix2569api.mercadopago.com/pix/123456789520400005303986540510.005802BR5913Test Store6009Sao Paulo62070503***6304E2CA",
                "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
                "transaction_amount": 100.00,
                "created_at": "2024-03-20T10:00:00Z",
                "updated_at": "2024-03-20T10:00:00Z",
                "payer": {
                    "email": "teste@email.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "identification": {
                        "type": "CPF",
                        "number": "191.191.191-00"
                    }
                }
            }
        }



class PaymentProviderDataResponse(BaseModel):
    provider_name: str
    mp_payment_id: Optional[str]
    mp_status: Optional[str]
    mp_status_detail: Optional[str]
    qr_code: Optional[str]
    qr_code_base64: Optional[str]
    ticket_url: Optional[str]
    date_of_expiration: Optional[str]

    class Config:
        orm_mode = True

class PaymentResponse(BaseModel):
    id: int
    transaction_amount: Decimal
    description: Optional[str]
    payment_method_id: str
    status: str
    provider_data: Optional[PaymentProviderDataResponse]

    class Config:
        orm_mode = True