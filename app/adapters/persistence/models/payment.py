from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.domain.models.payment import PaymentMethod, PaymentStatus

from .base import TimestampMixin


class Payment(TimestampMixin):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    amount = Column(Numeric(10, 2), nullable=False)
    paid_at = Column(DateTime, nullable=True)
    mp_response = Column(JSON, nullable=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    order = relationship("OrderModel", back_populates="payments")
