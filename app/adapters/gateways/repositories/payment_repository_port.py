from abc import ABC, abstractmethod

from app.adapters.gateways.repositories.mappers.payment_mapper import PaymentMapper


class PaymentRepositoryPort(ABC):
    @abstractmethod
    def save(self, payment: PaymentMapper) -> PaymentMapper:
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: int) -> PaymentMapper:
        """Return a payment by ID or None if not found."""
        pass

    @abstractmethod
    def get_payments_by_order_id(self, order_id: int) -> list[PaymentMapper]:
        """Return a list of payments for a given order ID."""
        pass

    @abstractmethod
    def get_payment_by_mp_id(self, mp_payment_id: str) -> PaymentMapper:
        """Return a payment by Mercado Pago ID or None if not found."""
        pass
