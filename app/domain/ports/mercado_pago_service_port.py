from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from app.domain.entities.payment import Payment


class MercadoPagoServicePort(ABC):
    """Port for Mercado Pago service in Domain Layer."""

    @abstractmethod
    def create_payment(self, payment: Payment) -> Dict[str, Any]:
        """Create a payment in Mercado Pago and return the response."""
        pass

    @abstractmethod
    def get_payment_status(self, mp_payment_id: str) -> Dict[str, Any]:
        """Get payment status from Mercado Pago."""
        pass

    @abstractmethod
    def refund_payment(self, mp_payment_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """Refund a payment in Mercado Pago."""
        pass
