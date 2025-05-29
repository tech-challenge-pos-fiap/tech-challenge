from typing import Any, Dict

from app.domain.ports.payment_port import PaymentPort


class CreatePixPaymentService:
    def __init__(self, payment_service: PaymentPort):
        self.payment_service = payment_service

    def execute(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.payment_service.create_pix_payment(payment_data)
