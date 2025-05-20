from abc import ABC, abstractmethod
from typing import Dict, Any

class PaymentPort(ABC):
    @abstractmethod
    def create_pix_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um pagamento PIX"""
        pass

    @abstractmethod
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Obtém o status de um pagamento"""
        pass
