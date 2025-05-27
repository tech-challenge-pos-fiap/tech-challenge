from datetime import datetime
from typing import Optional
from sqlalchemy.exc import NoResultFound

from sqlalchemy.orm import Session

from app.adapters.persistence.models.payment import Payment
from app.domain.models.payment import PaymentStatus


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        """Busca um pagamento pelo ID"""
        payment = self.db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise NoResultFound("Pagamento não encontrado.")
        payment.status = PaymentStatus.APPROVED
        payment.paid_at = datetime.now()
        return payment
