from app.adapters.external.mercado_pago.pix import MercadoPagoPixClient
from app.adapters.persistence.repositories.payment_repository import PaymentRepository
from app.domain.ports.payment_port import PaymentPort
from typing import Dict, Any
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime, UTC


class MercadoPagoPaymentService(PaymentPort):
    def __init__(self, client: MercadoPagoPixClient, db: Session):
        self.client = client
        self.repository = PaymentRepository(db)

    def create_pix_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        # Cria uma cópia do payment_data para não modificar o original
        payment_data = payment_data.copy()
        
        # Adiciona payment_method_id como "pix" por padrão
        payment_data["payment_method_id"] = "pix"
        
        # Converte Decimal para float para serialização JSON
        if isinstance(payment_data.get("transaction_amount"), Decimal):
            payment_data["transaction_amount"] = float(payment_data["transaction_amount"])
        
        # Obtém a resposta do Mercado Pago
        mp_response = self.client.create_pix_payment(payment_data)
        
        # Extrai o QR code do point_of_interaction
        point_of_interaction = mp_response.get("point_of_interaction", {})
        transaction_data = point_of_interaction.get("transaction_data", {})
        qr_code = transaction_data.get("qr_code", "")
        qr_code_base64 = transaction_data.get("qr_code_base64", "")
        
        # Adiciona os campos obrigatórios
        now = datetime.now(UTC).isoformat()
        response = {
            "id": mp_response["id"],
            "status": mp_response["status"],
            "transaction_amount": mp_response["transaction_amount"],
            "description": payment_data.get("description", ""),
            "payment_method_id": "pix",  # Garante que sempre será "pix"
            "created_at": now,
            "updated_at": now,
            "payer": {
                "email": payment_data.get("payer", {}).get("email", ""),
                "first_name": payment_data.get("payer", {}).get("first_name", ""),
                "last_name": payment_data.get("payer", {}).get("last_name", "")
            },
            "qr_code": qr_code,
            "qr_code_base64": qr_code_base64
        }
        
        return response

    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        payment = self.repository.get_payment_by_id(int(payment_id))
        if not payment:
            raise ValueError(f"Payment {payment_id} not found")
            
        return {
            "id": str(payment.id),
            "status": payment.status,
            "transaction_amount": float(payment.transaction_amount),
            "description": payment.description,
            "payment_method_id": payment.payment_method_id,
            "created_at": payment.created_at.isoformat(),
            "updated_at": payment.updated_at.isoformat(),
            "payer": {
                "email": payment.payer_email,
                "first_name": payment.payer_first_name,
                "last_name": payment.payer_last_name
            }
        }
