from app.adapters.external.mercado_pago.factory import get_payment_service
from app.application.services.create_payment_service import CreatePixPaymentService


def get_create_payment_service() -> CreatePixPaymentService:
    """Factory para criar o serviço de pagamento"""
    payment_service = get_payment_service()
    return CreatePixPaymentService(payment_service=payment_service)
