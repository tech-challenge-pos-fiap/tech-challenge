from datetime import UTC, datetime
from decimal import Decimal
from typing import Any, Dict

from sqlalchemy.orm import Session

from app.adapters.external.mercado_pago.pix import MercadoPagoPixClient
from app.adapters.persistence.models.payment import Payment
from app.adapters.persistence.repositories.payment_repository import PaymentRepository
from app.domain.models.payment import PaymentMethod
from app.domain.ports.payment_port import PaymentPort


class MercadoPagoPaymentService(PaymentPort):
    def __init__(self, client: MercadoPagoPixClient, db: Session):
        self.client = client
        self.repository = PaymentRepository(db)

    def create_pix_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        payment_data["payment_method_id"] = "pix"
        if isinstance(payment_data.get("transaction_amount"), Decimal):
            payment_data["transaction_amount"] = float(payment_data["transaction_amount"])
        payment_data_for_mp = payment_data.copy()
        payment_data_for_mp.pop("order_id", None)
        mp_response = self.client.create_pix_payment(payment_data_for_mp)

        payment = Payment(
            order_id=payment_data.get("order_id"),
            amount=Decimal(str(mp_response["transaction_amount"])),
            method=PaymentMethod.PIX,
            status=mp_response["status"],
            paid_at=None,
            mp_response=mp_response
        )
        saved_payment = self.repository.create_payment(payment)
        transaction_data = mp_response.get("point_of_interaction", {}).get("transaction_data", {})
        payer_data = payment_data.get("payer") or {}
        return {
            "id": saved_payment.id,
            "status": saved_payment.status,
            "transaction_amount": float(saved_payment.amount),
            "order_id": saved_payment.order_id,
            "description": payment_data.get("description", ""),
            "payment_method_id": "pix",
            "created_at": saved_payment.created_at.isoformat(),
            "updated_at": saved_payment.updated_at.isoformat(),
            "payer": {
                "email": payer_data.get("email"),
                "first_name": payer_data.get("first_name"),
                "last_name": payer_data.get("last_name"),
            } if payer_data else None,
            "qr_code": transaction_data.get("qr_code", ""),
            "qr_code_base64": transaction_data.get("qr_code_base64", "")
        }

    def get_payment_by_order_id(self, order_id: int) -> Dict[str, Any]:
        payment = self.repository.get_payment_by_order_id(order_id)
        return {
            "id": payment.id,
            "status": payment.status,
            "transaction_amount": float(payment.amount),
            "order_id": payment.order_id,
            "created_at": payment.created_at.isoformat(),
            "updated_at": payment.updated_at.isoformat(),
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
            "mp_response": payment.mp_response
        }
