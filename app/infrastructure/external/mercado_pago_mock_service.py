import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from app.domain.ports.mercado_pago_service_port import MercadoPagoServicePort
from app.domain.entities.payment import Payment


class MercadoPagoMockService(MercadoPagoServicePort):
    """Mock implementation of Mercado Pago service for testing and development."""
    
    def __init__(self, success_rate: float = 0.9):
        """
        Initialize the mock service.
        
        Args:
            success_rate: Probability of successful payment (0.0 to 1.0)
        """
        self.success_rate = success_rate
        self._payments = {}  # Store mock payments for status queries
    
    def create_payment(self, payment: Payment) -> Dict[str, Any]:
        """Create a mock payment in Mercado Pago."""
        import random
        
        # Simulate network delay
        import time
        time.sleep(0.1)
        
        # Generate mock payment ID
        mp_payment_id = f"mp_{uuid.uuid4().hex[:16]}"
        
        # Simulate success/failure based on success_rate
        is_successful = random.random() < self.success_rate
        
        if is_successful:
            status = "approved"
            status_detail = "accredited"
        else:
            status = "rejected"
            status_detail = "cc_rejected_bad_filled_security_code"
        
        # Create mock response
        mock_response = {
            "id": mp_payment_id,
            "status": status,
            "status_detail": status_detail,
            "transaction_amount": float(payment.transaction_amount),
            "transaction_amount_refunded": 0,
            "currency_id": "BRL",
            "payment_method_id": "pix",
            "payment_type_id": "credit_card",
            "date_approved": datetime.now(timezone.utc).isoformat() if is_successful else None,
            "date_created": datetime.now(timezone.utc).isoformat(),
            "date_last_updated": datetime.now(timezone.utc).isoformat(),
            "collector_id": 123456789,
            "payer": {
                "id": 123456789,
                "email": "test@example.com",
                "identification": {
                    "type": "CPF",
                    "number": "12345678901"
                }
            },
            "metadata": {
                "order_id": payment.order_id,
                "description": payment.description or "Payment for order"
            },
            "additional_info": {
                "items": [
                    {
                        "id": "item_1",
                        "title": "Order Payment",
                        "quantity": 1,
                        "unit_price": float(payment.transaction_amount)
                    }
                ]
            }
        }
        
        # Store payment for status queries
        self._payments[mp_payment_id] = mock_response
        
        return mock_response
    
    def get_payment_status(self, mp_payment_id: str) -> Dict[str, Any]:
        """Get payment status from mock Mercado Pago."""
        if mp_payment_id not in self._payments:
            raise ValueError(f"Payment {mp_payment_id} not found")
        
        return self._payments[mp_payment_id]
    
    def refund_payment(self, mp_payment_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """Refund a payment in mock Mercado Pago."""
        if mp_payment_id not in self._payments:
            raise ValueError(f"Payment {mp_payment_id} not found")
        
        original_payment = self._payments[mp_payment_id]
        refund_amount = amount or original_payment["transaction_amount"]
        
        mock_refund_response = {
            "id": f"refund_{uuid.uuid4().hex[:16]}",
            "payment_id": mp_payment_id,
            "amount": refund_amount,
            "status": "approved",
            "date_created": datetime.now(timezone.utc).isoformat(),
            "unique_sequence_number": f"refund_{uuid.uuid4().hex[:8]}"
        }
        
        return mock_refund_response
    
    def set_success_rate(self, success_rate: float) -> None:
        """Update the success rate for testing different scenarios."""
        self.success_rate = max(0.0, min(1.0, success_rate))
    
    def clear_payments(self) -> None:
        """Clear stored payments (useful for testing)."""
        self._payments.clear() 