import os
from app.adapters.external.mercado_pago.pix import MercadoPagoPixClient
from app.adapters.external.mercado_pago.payment_service import MercadoPagoPaymentService


def get_payment_service():
    client = MercadoPagoPixClient()
    return MercadoPagoPaymentService(client)