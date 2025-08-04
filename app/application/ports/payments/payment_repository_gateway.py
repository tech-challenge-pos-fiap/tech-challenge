from abc import ABC, abstractmethod

from app.domain.entities.payment import Payment


class PaymentRepositoryGatewayPort(ABC):
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        """Saves a payment entity."""
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: int) -> Payment:
        """Retrieves a payment entity by its ID."""
        pass

    @abstractmethod
    def get_payments_by_order_id(self, order_id: int) -> list[Payment]:
        """Retrieves a list of payment entities by order ID."""
        pass

    @abstractmethod
    def get_payment_by_mp_id(self, mp_payment_id: str) -> Payment:
        """Retrieves a payment entity by Mercado Pago ID."""
        pass
