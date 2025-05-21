from dataclasses import dataclass
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

@dataclass
class Payment:
    id: Optional[int]
    transaction_amount: Decimal
    description: Optional[str]
    payment_method_id: str
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
