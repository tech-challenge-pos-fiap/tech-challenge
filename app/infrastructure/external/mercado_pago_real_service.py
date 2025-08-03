import os
from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException

from app.domain.ports.mercado_pago_service_port import MercadoPagoServicePort
from app.domain.entities.payment import Payment


class MercadoPagoRealService(MercadoPagoServicePort):
    """Real implementation of Mercado Pago service for production."""
    
    def __init__(self):
        self.base_url = os.getenv("MP_PAYMENT_URL", "https://api.mercadopago.com/v1/payments")
        self.access_token = os.getenv("MP_ACCESS_TOKEN")
        self.idempotency_key = os.getenv("MP_IDEMPOTENCY_KEY")
        
        if not self.access_token:
            raise ValueError("MP_ACCESS_TOKEN environment variable is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Idempotency-Key": self.idempotency_key or ""
        }
    
    def create_payment(self, payment: Payment) -> Dict[str, Any]:
        """Create a real payment in Mercado Pago."""
        payment_data = {
            "transaction_amount": float(payment.transaction_amount),
            "token": "card_token",  # This would come from frontend
            "description": payment.description or f"Payment for order {payment.order_id}",
            "installments": 1,
            "payment_method_id": "pix",
            "payer": {
                "email": "test@example.com"  # This would come from order
            },
            "metadata": {
                "order_id": payment.order_id,
                "description": payment.description
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=payment_data,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to create payment in Mercado Pago: {str(e)}")
    
    def get_payment_status(self, mp_payment_id: str) -> Dict[str, Any]:
        """Get payment status from Mercado Pago."""
        try:
            response = requests.get(
                f"{self.base_url}/{mp_payment_id}",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to get payment status from Mercado Pago: {str(e)}")
    
    def refund_payment(self, mp_payment_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """Refund a payment in Mercado Pago."""
        refund_data = {}
        if amount is not None:
            refund_data["amount"] = amount
        
        try:
            response = requests.post(
                f"{self.base_url}/{mp_payment_id}/refunds",
                json=refund_data,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to refund payment in Mercado Pago: {str(e)}") 