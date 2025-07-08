from app.application.ports.payments.payment_repository_gateway import PaymentRepositoryGatewayPort
from app.domain.entities.payment import Payment


class GetPaymentByIdUseCase:
    def __init__(self, payment_repository: PaymentRepositoryGatewayPort):
        self.payment_repository = payment_repository

    def execute(self, payment_id: int) -> Payment:
        return self.payment_repository.get_payment_by_id(payment_id)
