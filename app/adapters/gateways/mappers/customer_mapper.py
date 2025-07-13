from dataclasses import dataclass
from app.domain.entities.customer import Customer


@dataclass
class CustomerMapper:
    id: int
    name: str
    email: str
    cpf: str

    @classmethod
    def from_entity(cls, customer: Customer) -> 'CustomerMapper':
        return cls(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            cpf=customer.cpf.value if customer.cpf else None
        )

    def to_entity(self) -> Customer:
        return Customer(
            id=self.id,
            name=self.name,
            email=self.email,
            cpf=self.cpf
        )
