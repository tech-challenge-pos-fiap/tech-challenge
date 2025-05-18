from app.adapters.external.mercado_pago.pix import MercadoPagoPixClient
from app.application.ports.payment import PaymentPort


class MercadoPagoPaymentService(PaymentPort):
    def __init__(self, client: MercadoPagoPixClient):
        self.client = client

    def create_pix_payment(self, payment_data: dict) -> dict:
        return self.client.create_pix_payment(payment_data)
