from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Dict, Any


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    IN_PROCESS = "IN_PROCESS"
    ERROR = "ERROR"


class PaymentMethod(str, Enum):
    PIX = "PIX"
    CREDIT_CARD = "CREDIT_CARD"
    BOLETO = "BOLETO"


@dataclass
class Payment:
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
