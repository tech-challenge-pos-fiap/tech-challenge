from sqlalchemy.orm import Session
from app.domain.models.customer import Customer
from app.domain.value_objects.cpf import CPF
from app.application.ports.customer_repository_port import CustomerRepositoryPort
from app.adapters.persistence.models.customer import CustomerModel


class CustomerRepository(CustomerRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: CustomerModel) -> Customer:
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            cpf=CPF(model.cpf) if model.cpf else None
        )

    def save(self, customer: Customer) -> Customer:
        instance = CustomerModel(
            name=customer.name,
            email=customer.email,
            cpf=str(customer.cpf) if customer.cpf else None
        )

        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return self._to_domain(instance)

    def get_by_email(self, email: str) -> Customer | None:
        instance = self.db.query(CustomerModel).filter_by(email=email).first()
        return self._to_domain(instance) if instance else None

    def get_by_cpf(self, cpf: CPF) -> Customer | None:
        instance = self.db.query(CustomerModel).filter_by(cpf=str(cpf)).first()
        return self._to_domain(instance) if instance else None
