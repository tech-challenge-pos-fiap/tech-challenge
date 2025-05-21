from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.customer import Customer
from app.domain.value_objects.cpf import CPF


class CustomerRepositoryPort(ABC):

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        """Persist a customer and return it (possibly with ID populated)."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Return a customer by email or None if not found."""
        pass

    @abstractmethod
    def get_by_cpf(self, cpf: CPF) -> Optional[Customer]:
        """Return a customer by CPF or None if not found."""
        pass
