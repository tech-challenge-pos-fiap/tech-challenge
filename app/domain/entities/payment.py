from dataclasses import dataclass
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
    id: Optional[int]
    transaction_amount: Decimal
    description: Optional[str]
    payment_method_id: str
    status: PaymentStatus
    order_id: int
