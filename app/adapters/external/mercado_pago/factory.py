from app.adapters.external.mercado_pago.pix import MercadoPagoPixClient
from app.adapters.external.mercado_pago.payment_service import MercadoPagoPaymentService
from app.config.db import get_db
from app.domain.ports.payment_port import PaymentPort
from fastapi import Depends
from sqlalchemy.orm import Session


def get_payment_service(db: Session = Depends(get_db)) -> PaymentPort:
    """Factory para criar o serviço de pagamento do Mercado Pago"""
    client = MercadoPagoPixClient()
    return MercadoPagoPaymentService(client=client, db=db)