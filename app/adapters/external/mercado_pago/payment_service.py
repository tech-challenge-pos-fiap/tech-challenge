from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Dict

from app.adapters.persistence.models.payment import Payment
from app.domain.models.payment import PaymentMethod, PaymentStatus
from sqlalchemy.orm import Session

from app.adapters.external.mercado_pago.pix import MercadoPagoPixClient
from app.adapters.persistence.repositories.payment_repository import PaymentRepository
from app.domain.ports.payment_port import PaymentPort


class MercadoPagoPaymentService(PaymentPort):
    def __init__(self, client: MercadoPagoPixClient, db: Session):
        self.client = client
        self.repository = PaymentRepository(db)

    def create_pix_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        payment_data = payment_data.copy()
        payment_data["payment_method_id"] = "pix"
        if isinstance(payment_data.get("transaction_amount"), Decimal):
            payment_data["transaction_amount"] = float(payment_data["transaction_amount"])

        mp_response = self.client.create_pix_payment(payment_data)
        payment = Payment(
            # order_id=payment_data["order_id"],
            amount=Decimal(str(mp_response["transaction_amount"])),
            method=PaymentMethod.PIX,
            status=mp_response["status"],
            paid_at=None,
            mp_response=mp_response
        )
        saved_payment = self.repository.create_payment(payment)

        transaction_data = mp_response.get("point_of_interaction", {}).get("transaction_data", {})

        return {
            "id": saved_payment.id,
            "status": saved_payment.status,
            "transaction_amount": float(saved_payment.amount),
            "description": payment_data.get("description", ""),
            "payment_method_id": "pix",
            "created_at": saved_payment.created_at.isoformat(),
            "updated_at": saved_payment.updated_at.isoformat(),
            "payer": {
                "email": payment_data.get("payer", {}).get("email", ""),
                "first_name": payment_data.get("payer", {}).get("first_name", ""),
                "last_name": payment_data.get("payer", {}).get("last_name", "")
            },
            "qr_code": transaction_data.get("qr_code", ""),
            "qr_code_base64": transaction_data.get("qr_code_base64", "")
        }
