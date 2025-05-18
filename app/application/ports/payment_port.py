from abc import ABC, abstractmethod

class PaymentPort(ABC):
    @abstractmethod
    def create_pix_payment(self, payment_data: dict) -> dict:
        pass

    @abstractmethod
    def get_payment_status(self, payment_id: int) -> dict:
        pass
