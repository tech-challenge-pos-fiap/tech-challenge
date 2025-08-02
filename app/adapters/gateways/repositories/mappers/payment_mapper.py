from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.domain.entities.payment import Payment, PaymentMethod, PaymentStatus


@dataclass
class PaymentMapper:
    transaction_amount: Decimal
    payment_method: PaymentMethod
    status: PaymentStatus
    description: Optional[str]
    paid_at: datetime
    order_id: int
    id: Optional[int] = field(default=None)

    @classmethod
    def from_entity(cls, payment) -> "PaymentMapper":
        return cls(
            id=payment.id,
            transaction_amount=payment.transaction_amount,
            payment_method=payment.payment_method,
            status=payment.status,
            description=payment.description,
            paid_at=payment.paid_at,
            order_id=payment.order_id,
        )

    def to_entity(self) -> Payment:
        return Payment(
            id=self.id,
            transaction_amount=self.transaction_amount,
            payment_method=self.payment_method,
            status=self.status,
            description=self.description,
            paid_at=self.paid_at,
            order_id=self.order_id,
        )
