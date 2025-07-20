from dataclasses import asdict
from typing import Any

from app.domain.entities.payment import Payment


class PaymentPresenter:
    @classmethod
    def present(cls, payment: Payment) -> dict[str, Any]:
        return asdict(payment)
