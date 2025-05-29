from typing import Any, Dict

from app.adapters.external.mercado_pago.payment_service import MercadoPagoPaymentService


class ListPaymentService:
    def __init__(self, payment_service: MercadoPagoPaymentService):
        self.payment_service = payment_service

    def get_payment_by_id(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.payment_service.get_payment_by_id(payment_data)

    def get_payment_by_order_id(self, order_id: int) -> Dict[str, Any]:
        return self.payment_service.get_payment_by_order_id(order_id)
