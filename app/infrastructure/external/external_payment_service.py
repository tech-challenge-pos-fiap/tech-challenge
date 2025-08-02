from app.adapters.gateways.services.payment_process_service import PaymentProcessServicePort


class ExternalPaymentProcessService(PaymentProcessServicePort):
    def process_payment(self, payment_data: dict) -> bool:
        return True
