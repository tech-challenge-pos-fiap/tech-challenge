from app.application.ports.payments.payment_repository_gateway import PaymentRepositoryGatewayPort
from app.domain.entities.payment import Payment


class GetPaymentsByOrderIdUseCase:
    def __init__(self, payment_repository: PaymentRepositoryGatewayPort):
        self.payment_repository = payment_repository

    def execute(self, order_id: int) -> list[Payment]:
        return self.payment_repository.get_payments_by_order_id(order_id)
