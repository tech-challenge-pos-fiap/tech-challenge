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
            mp_payment_id=payment.mp_payment_id,
            mp_status=payment.mp_status,
            mp_status_detail=payment.mp_status_detail,
            mp_response=payment.mp_response,
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
            mp_payment_id=instance.mp_payment_id,
            mp_status=instance.mp_status,
            mp_status_detail=instance.mp_status_detail,
            mp_response=instance.mp_response,
        )

    def save(self, payment: PaymentMapper) -> PaymentMapper:
        if payment.id:
            payment_model = self.session.query(PaymentModel).filter(PaymentModel.id == payment.id).first()
            if payment_model:
                payment_model.transaction_amount = payment.transaction_amount
                payment_model.payment_method = payment.payment_method
                payment_model.status = payment.status
                payment_model.description = payment.description
                payment_model.paid_at = payment.paid_at
                payment_model.order_id = payment.order_id
                payment_model.mp_payment_id = payment.mp_payment_id
                payment_model.mp_status = payment.mp_status
                payment_model.mp_status_detail = payment.mp_status_detail
                payment_model.mp_response = payment.mp_response
                self.session.commit()
                self.session.refresh(payment_model)
                return self._model_to_mapper(payment_model)

        # Create new payment
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

    def get_payment_by_mp_id(self, mp_payment_id: str) -> PaymentMapper:
        payment_model = self.session.query(PaymentModel).filter(PaymentModel.mp_payment_id == mp_payment_id).first()
        return self._model_to_mapper(payment_model) if payment_model else None
