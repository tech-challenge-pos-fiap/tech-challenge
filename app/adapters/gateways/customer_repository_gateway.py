from app.adapters.gateways.mappers.customer_mapper import CustomerMapper
from app.adapters.gateways.repositories.customer_repository_port import CustomerRepositoryPort
from app.application.ports.customers.customer_repository_gateway import CustomerRepositoryGatewayPort
from app.domain.entities.customer import Customer


class CustomerRepositoryGateway(CustomerRepositoryGatewayPort):
    def __init__(self, repository: CustomerRepositoryPort):
        self.repository = repository

    def save(self, customer: Customer) -> Customer:
        customer_mapper = CustomerMapper.from_entity(customer)
        saved_customer = self.repository.save(customer_mapper)
        return saved_customer.to_entity()

    def get_by_email(self, email):
        customer_mapper = self.repository.get_by_email(email)
        return customer_mapper.to_entity()

    def get_by_cpf(self, cpf):
        customer_mapper = self.repository.get_by_cpf(cpf)
        return customer_mapper.to_entity() if customer_mapper else None
