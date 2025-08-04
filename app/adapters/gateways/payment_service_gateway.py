from dataclasses import asdict
from typing import Any, Dict

from app.adapters.gateways.services.payment_process_service import PaymentProcessServicePort
from app.application.ports.payments.payment_service_gateway import PaymentServiceGatewayPort
from app.domain.entities.payment import Payment, PaymentStatus
from app.domain.ports.mercado_pago_service_port import MercadoPagoServicePort


class PaymentServiceGateway(PaymentServiceGatewayPort):
    def __init__(self, validation_service: PaymentProcessServicePort, mp_service: MercadoPagoServicePort):
        self.validation_service = validation_service
        self.mp_service = mp_service

    def process_payment(self, payment: Payment) -> bool:
        """Process payment using validation service and Mercado Pago."""
        payment_details = asdict(payment)
        validation_success = self.validation_service.process_payment(payment_details)

        if not validation_success:
            payment.status = PaymentStatus.REJECTED
            payment.mp_response = {"error": "Payment validation failed"}
            return False

        try:
            mp_response = self.mp_service.create_payment(payment)

            payment.mp_payment_id = mp_response.get("id")
            payment.mp_status = mp_response.get("status")
            payment.mp_status_detail = mp_response.get("status_detail")
            payment.mp_response = mp_response

            if mp_response.get("status") == "approved":
                payment.status = PaymentStatus.APPROVED
            elif mp_response.get("status") in ["rejected", "cancelled"]:
                payment.status = PaymentStatus.REJECTED
            else:
                payment.status = PaymentStatus.IN_PROCESS

            return True

        except Exception as e:
            payment.status = PaymentStatus.IN_PROCESS
            payment.mp_response = {"error": str(e)}
            return False

    def get_payment_status(self, mp_payment_id: str) -> Dict[str, Any]:
        """Get payment status from Mercado Pago."""
        return self.mp_service.get_payment_status(mp_payment_id)

    def refund_payment(self, mp_payment_id: str, amount: float = None) -> Dict[str, Any]:
        """Refund a payment in Mercado Pago."""
        return self.mp_service.refund_payment(mp_payment_id, amount)
