from typing import List, Optional

from sqlalchemy.orm import Session

from app.adapters.persistence.models.payment import Payment, PaymentProviderData


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment: Payment) -> Payment:
        """Cria um novo pagamento"""
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def save_mp_response(self, payment_id: int, mp_data: dict) -> PaymentProviderData:
        """Salva a resposta do Mercado Pago para um pagamento"""
        mp_response = PaymentProviderData(
            payment_id=payment_id,
            provider_name="mercado_pago",
            mp_payment_id=str(mp_data["id"]),
            mp_status=mp_data["status"],
            mp_status_detail=mp_data["status_detail"],
            qr_code=mp_data["point_of_interaction"]["transaction_data"].get("qr_code"),
            qr_code_base64=mp_data["point_of_interaction"]["transaction_data"].get("qr_code_base64"),
            ticket_url=mp_data["point_of_interaction"]["transaction_data"].get("ticket_url"),
            date_of_expiration=mp_data.get("date_of_expiration")
        )
        self.db.add(mp_response)
        self.db.commit()
        self.db.refresh(mp_response)
        return mp_response

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        """Busca um pagamento pelo ID"""
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_payment_by_mp_id(self, mp_payment_id: str) -> Optional[Payment]:
        """Busca um pagamento pelo ID do Mercado Pago"""
        return self.db.query(Payment).join(PaymentProviderData).filter(
            PaymentProviderData.mp_payment_id == mp_payment_id
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
