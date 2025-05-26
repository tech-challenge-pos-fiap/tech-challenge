from typing import Any, Dict

from app.adapters.external.mercado_pago.payment_service import MercadoPagoPaymentService


class GetPixPaymentService:
    def __init__(self, payment_service: MercadoPagoPaymentService):
        self.payment_service = payment_service

    def execute(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.payment_service.get_payment_status(payment_data)
