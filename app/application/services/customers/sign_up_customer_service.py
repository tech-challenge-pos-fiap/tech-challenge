from app.application.ports.customer_repository_port import CustomerRepositoryPort
from app.domain.models.customer import Customer


class SignUpCustomerService:
    def __init__(self, repository: CustomerRepositoryPort):
        self.repository = repository

    def execute(self, name: str, email: str) -> Customer:
        existing = self.repository.get_by_email(email)
        if existing:
            return existing
        customer = Customer(name=name, email=email)
        return self.repository.save(customer)
