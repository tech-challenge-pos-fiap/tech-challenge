from app.application.ports.customers.customer_repository_gateway import CustomerRepositoryGatewayPort
from app.domain.entities.customer import Customer
from app.domain.value_objects.cpf import CPF


class IdentifyCustomerUseCase:
    def __init__(self, repository_gateway: CustomerRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, cpf_str: str) -> Customer:
        cpf = CPF(cpf_str)
        existing = self.repository_gateway.get_by_cpf(cpf)
        if existing:
            return existing
        customer = Customer(cpf=cpf)
        return self.repository_gateway.save(customer)
