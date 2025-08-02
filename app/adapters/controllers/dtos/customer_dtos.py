from dataclasses import dataclass


@dataclass
class CustomerSignUpDTO:
    name: str
    email: str


@dataclass
class CustomerIdentifyDTO:
    cpf: str
