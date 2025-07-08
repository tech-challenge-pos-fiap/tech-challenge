from dataclasses import dataclass
from typing import Optional

from app.domain.value_objects.cpf import CPF


@dataclass
class Customer:
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[CPF] = None
