from fastapi import APIRouter, Depends
from app.adapters.api.dtos.customer_dto import (
    SignUpRequest, IdentifyByCPFRequest, CustomerResponse
)
from app.application.services.sign_up_customer_service import SignUpCustomerService
from app.application.services.identify_customer_service import IdentifyCustomerService
from app.config.depencencies import get_sign_up_service, get_identify_by_cpf_service

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/signup", response_model=CustomerResponse)
def sign_up(
    payload: SignUpRequest,
    service: SignUpCustomerService = Depends(get_sign_up_service)
):
    customer = service.execute(name=payload.name, email=payload.email)
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        cpf=str(customer.cpf) if customer.cpf else None
    )


@router.post("/identify", response_model=CustomerResponse)
def identify_by_cpf(
    payload: IdentifyByCPFRequest,
    service: IdentifyCustomerService = Depends(get_identify_by_cpf_service)
):
    customer = service.execute(cpf_str=payload.cpf)
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        cpf=str(customer.cpf) if customer.cpf else None
    )
