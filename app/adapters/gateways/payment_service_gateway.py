from dataclasses import asdict
from app.application.ports.payments.payment_service_gateway import PaymentServiceGatewayPort
from app.domain.entities.payment import Payment
from app.adapters.gateways.services.payment_process_service import PaymentProcessServicePort


class PaymentServiceGateway(PaymentServiceGatewayPort):
    def __init__(self, service: PaymentProcessServicePort):
        self.service = service

    def process_payment(self, payment: Payment) -> bool:
        payment_details = asdict(payment)
        return self.service.process_payment(payment_details)
