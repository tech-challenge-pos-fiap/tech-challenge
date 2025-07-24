from app.adapters.gateways.repositories.mappers.payment_mapper import PaymentMapper
from app.adapters.gateways.repositories.payment_repository_port import PaymentRepositoryPort
from app.application.ports.payments.payment_repository_gateway import PaymentRepositoryGatewayPort
from app.domain.entities.payment import Payment


class PaymentRepositoryGateway(PaymentRepositoryGatewayPort):
    def __init__(self, repository: PaymentRepositoryPort):
        self.repository = repository

    def save(self, payment: Payment) -> Payment:
        """Saves a payment entity."""
        payment_mapper = PaymentMapper.from_entity(payment)
        saved_payment = self.repository.save(payment_mapper)
        return saved_payment.to_entity()

    def get_payment_by_id(self, payment_id):
        payment_mapper = self.repository.get_payment_by_id(payment_id)
        return payment_mapper.to_entity() if payment_mapper else None

    def get_payments_by_order_id(self, order_id: int) -> list[Payment]:
        payment_mappers = self.repository.get_payments_by_order_id(order_id)
        return [payment_mapper.to_entity() for payment_mapper in payment_mappers]
