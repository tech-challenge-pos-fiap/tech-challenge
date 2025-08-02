from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class PaymentStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    IN_PROCESS = "in_process"
    ERROR = "error"


class PaymentMethod(str, Enum):
    PIX = "pix"
    CREDIT_CARD = "credit_card"
    BOLETO = "boleto"


@dataclass
class Payment:
    transaction_amount: Decimal
    payment_method: PaymentMethod
    status: PaymentStatus
    description: Optional[str]
    paid_at: datetime
    order_id: int
    id: Optional[int] = field(default=None)

    @classmethod
    def create(
        cls,
        transaction_amount: Decimal,
        description: Optional[str],
        order_id: int,
    ) -> "Payment":
        status = PaymentStatus.PENDING
        payment_method = PaymentMethod.PIX
        paid_at = datetime.now()

        return cls(
            transaction_amount=transaction_amount,
            payment_method=payment_method,
            status=status,
            description=description,
            paid_at=paid_at,
            order_id=order_id,
        )
