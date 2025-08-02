from typing import Any

from app.domain.entities.customer import Customer


class CustomerPresenter:
    @classmethod
    def present(cls, customer: Customer) -> dict[str, Any]:
        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "cpf": customer.cpf,
        }
