from abc import ABC, abstractmethod
from typing import Any, Dict


class PaymentPort(ABC):
    @abstractmethod
    def create_pix_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um pagamento PIX"""
        pass
