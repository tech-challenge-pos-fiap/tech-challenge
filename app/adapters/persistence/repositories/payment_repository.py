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
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_payment_by_mp_id(self, mp_payment_id: str) -> Optional[Payment]:
        """Busca um pagamento pelo ID do Mercado Pago"""
        return self.db.query(Payment).filter(
            Payment.mp_payment_id == mp_payment_id
        ).first()

    def update_status(self, payment_id: int, status: str, error_message: Optional[str] = None) -> Optional[Payment]:
        """Atualiza o status de um pagamento"""
        payment = self.get_payment_by_id(payment_id)
        if payment:
            payment.status = status
            if error_message and hasattr(payment, "error_message"):
                payment.error_message = error_message
            self.db.commit()
            self.db.refresh(payment)
        return payment

    def list_by_status(self, status: str) -> List[Payment]:
        """Lista pagamentos por status"""
        return self.db.query(Payment).filter(Payment.status == status).all()
