from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from .base import TimestampMixin


class Payment(TimestampMixin):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    transaction_amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String, nullable=True)
    payment_method_id = Column(String, default="pix", nullable=False)
    status = Column(String, nullable=False)


class PaymentProviderData(TimestampMixin):
    __tablename__ = "payment_provider_data"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    provider_name = Column(String, nullable=False)  # ex: 'mercado_pago', 'stripe'

    # Campos genéricos para gateways
    mp_payment_id = Column(String, nullable=True)
    mp_status = Column(String, nullable=True)
    mp_status_detail = Column(String, nullable=True)
    qr_code = Column(Text, nullable=True)
    qr_code_base64 = Column(Text, nullable=True)
    ticket_url = Column(Text, nullable=True)
    date_of_expiration = Column(DateTime, nullable=True)

    # payment = relationship("Payment", back_populates="provider_data")



# class MPResponse(BaseModel):
#     mp_payment_id: str
#     mp_issuer_id: Optional[str] = None
#     mp_status: str
#     mp_status_detail: str
#     qr_code: str
#     qr_code_base64: str
#     ticket_url: str

#     class Config:
#         from_attributes = True


# class PaymentResponse(BaseModel):
#     id: int
#     transaction_amount: Decimal
#     description: Optional[str] = None
#     payment_method_id: str
#     status: str
#     created_at: str
#     mp_response: Optional[MPResponse] = None

#     class Config:
#         from_attributes = True
