from sqlalchemy.orm import Session

from app.adapters.gateways.repositories.mappers.payment_mapper import PaymentMapper
from app.adapters.gateways.repositories.payment_repository_port import PaymentRepositoryPort
from app.infrastructure.persistence.models.payment import PaymentModel


class PaymentRepository(PaymentRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def _mapper_to_model(self, payment: PaymentMapper) -> PaymentModel:
        return PaymentModel(
            id=payment.id,
            transaction_amount=payment.transaction_amount,
            payment_method=payment.payment_method,
            status=payment.status,
            description=payment.description,
            paid_at=payment.paid_at,
            order_id=payment.order_id,
        )

    def _model_to_mapper(self, instance: PaymentModel) -> PaymentMapper:
        return PaymentMapper(
            id=instance.id,
            transaction_amount=instance.transaction_amount,
            payment_method=instance.payment_method,
            status=instance.status,
            description=instance.description,
            paid_at=instance.paid_at,
            order_id=instance.order_id,
        )

    def save(self, payment: PaymentMapper) -> PaymentMapper:
        payment_model = self._mapper_to_model(payment)
        self.session.add(payment_model)
        self.session.commit()
        self.session.refresh(payment_model)
        return self._model_to_mapper(payment_model)

    def get_payment_by_id(self, payment_id):
        payment_model = self.session.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
        return self._model_to_mapper(payment_model) if payment_model else None

    def get_payments_by_order_id(self, order_id):
        payment_models = self.session.query(PaymentModel).filter(PaymentModel.order_id == order_id).all()
        return [self._model_to_mapper(payment_model) for payment_model in payment_models] if payment_models else []
