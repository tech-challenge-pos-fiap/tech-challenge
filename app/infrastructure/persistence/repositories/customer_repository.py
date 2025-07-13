from sqlalchemy.orm import Session

from app.adapters.gateways.repositories.customer_repository_port import CustomerRepositoryPort
from app.adapters.gateways.mappers.customer_mapper import CustomerMapper
from app.infrastructure.persistence.models.customer import CustomerModel


class CustomerRepository(CustomerRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def _mapper_to_model(self, customer: CustomerMapper) -> CustomerModel:
        return CustomerModel(
            name=customer.name,
            email=customer.email,
            cpf=customer.cpf
        )

    def _model_to_mapper(self, instance: CustomerModel) -> CustomerMapper:
        return CustomerMapper(
            id=instance.id,
            name=instance.name,
            email=instance.email,
            cpf=instance.cpf
        )

    def save(self, customer: CustomerMapper) -> CustomerMapper:
        instance = self._mapper_to_model(customer)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return self._model_to_mapper(instance)

    def get_by_email(self, email: str) -> CustomerMapper:
        instance = self.session.query(CustomerModel).filter_by(email=email).first()
        return self._model_to_mapper(instance) if instance else None

    def get_by_cpf(self, cpf: str) -> CustomerMapper:
        instance = self.session.query(CustomerModel).filter_by(cpf=cpf).first()
        return self._model_to_mapper(instance) if instance else None
