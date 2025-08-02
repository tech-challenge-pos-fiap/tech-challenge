from abc import ABC, abstractmethod

from app.domain.entities.payment import Payment


class PaymentServiceGatewayPort(ABC):
    @abstractmethod
    def process_payment(self, payment: Payment) -> bool:
        """Process the payment and return the result."""
        pass
