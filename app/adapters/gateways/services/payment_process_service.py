from abc import ABC, abstractmethod


class PaymentProcessServicePort(ABC):
    @abstractmethod
    def process_payment(self, payment_data: dict) -> bool:
        """Process the payment and return if it was successful."""
        pass
