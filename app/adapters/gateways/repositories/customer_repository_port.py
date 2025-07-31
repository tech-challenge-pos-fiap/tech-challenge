from abc import ABC, abstractmethod

from app.adapters.gateways.repositories.mappers.customer_mapper import CustomerMapper


class CustomerRepositoryPort(ABC):
    @abstractmethod
    def save(self, customer: CustomerMapper) -> CustomerMapper:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> CustomerMapper:
        """Return a customer by email or None if not found."""
        pass

    @abstractmethod
    def get_by_cpf(self, cpf: str) -> CustomerMapper:
        """Return a customer by CPF or None if not found."""
        pass
