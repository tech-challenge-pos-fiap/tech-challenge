from typing import Any, Dict

from app.adapters.external.mercado_pago.payment_service import MercadoPagoPaymentService


class CreatePixPaymentService:
    def __init__(self, payment_service: MercadoPagoPaymentService):
        self.payment_service = payment_service

    def execute(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        # O serviço do Mercado Pago já retorna a resposta formatada corretamente
        return self.payment_service.create_pix_payment(payment_data)
