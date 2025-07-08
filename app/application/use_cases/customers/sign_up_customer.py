from app.application.ports.customers.customer_repository_gateway import CustomerRepositoryGatewayPort
from app.domain.models.customer import Customer


class SignUpCustomerUseCase:
    def __init__(self, repository_gateway: CustomerRepositoryGatewayPort):
        self.repository_gateway = repository_gateway

    def execute(self, name: str, email: str) -> Customer:
        existing = self.repository_gateway.get_by_email(email)
        if existing:
            return existing
        customer = Customer(name=name, email=email)
        return self.repository_gateway.save(customer)
