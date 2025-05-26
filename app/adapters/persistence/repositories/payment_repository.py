from typing import List, Optional

from app.domain.models.payment import PaymentMethod, PaymentStatus
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.adapters.persistence.models.payment import Payment


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
        if payment:
            payment.status = PaymentStatus.APPROVED
            payment.paid_at = datetime.now() 
        return payment
