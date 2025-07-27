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

    def get_payment_by_order_id(self, order_id: int) -> list[Payment]:
        """
            Busca os pagamentos pelo order_id (retornando uma lista) e atualiza os campos “status” e “paid_at”
        """
        payments = self.db.query(Payment).filter(Payment.order_id == order_id).all()
        if not payments:
            raise NoResultFound(f"Order {order_id} não possui pagamentos.")
        for payment in payments:
            payment.status = PaymentStatus.APPROVED
            payment.paid_at = datetime.now()
        return payments
