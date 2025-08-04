from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

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
    mp_payment_id: Optional[str] = field(default=None)
    mp_status: Optional[str] = field(default=None)
    mp_status_detail: Optional[str] = field(default=None)
    mp_response: Optional[Dict[str, Any]] = field(default=None)

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
            mp_payment_id=payment.mp_payment_id,
            mp_status=payment.mp_status,
            mp_status_detail=payment.mp_status_detail,
            mp_response=payment.mp_response,
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
            mp_payment_id=self.mp_payment_id,
            mp_status=self.mp_status,
            mp_status_detail=self.mp_status_detail,
            mp_response=self.mp_response,
        )
