from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.payment import PaymentMethod, PaymentStatus

from .base import TimestampMixin


class PaymentModel(TimestampMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(
            PaymentMethod,
            name="paymentmethod",
            native_enum=True,
            values_callable=lambda x: [e.value for e in PaymentMethod]
        ),
        nullable=False,
    )
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(
            PaymentStatus,
            name="paymentstatus",
            native_enum=True,
            values_callable=lambda x: [e.value for e in PaymentStatus]
        ),
        default=PaymentStatus.PENDING,
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    mp_response: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    order_id: Mapped[Optional[int]] = mapped_column(ForeignKey('orders.id'), nullable=True)
    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="payments")
