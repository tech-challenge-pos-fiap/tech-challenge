from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, StringConstraints


class SignUpRequest(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    email: EmailStr


class IdentifyByCPFRequest(BaseModel):
    cpf: Annotated[str, StringConstraints(pattern=r'^\d{11}$')]


class CustomerResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
