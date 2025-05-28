from app.application.ports.customer_repository_port import CustomerRepositoryPort
from app.domain.models.customer import Customer
from app.domain.value_objects.cpf import CPF


class IdentifyCustomerService:
    def __init__(self, repository: CustomerRepositoryPort):
        self.repository = repository

    def execute(self, cpf_str: str) -> Customer:
        cpf = CPF(cpf_str)
        existing = self.repository.get_by_cpf(cpf)
        if existing:
            return existing
        customer = Customer(cpf=cpf)
        return self.repository.save(customer)
