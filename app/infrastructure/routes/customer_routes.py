from fastapi import APIRouter, Depends

from app.adapters.controllers.customers.customer_identify_controller import CustomerIdentifyController
from app.adapters.controllers.customers.customer_sign_up_controller import CustomerSignUpController
from app.adapters.controllers.dtos.customer_dtos import CustomerIdentifyDTO, CustomerSignUpDTO
from app.infrastructure.dependencies.customer_dependencies import (
    get_identify_customer_controller,
    get_sign_up_customer_controller,
)
from app.infrastructure.routes.schemas.customer_schemas import (
    CustomerIdentifyByCPFRequestSchema,
    CustomerResponseSchema,
    CustomerSignUpRequestSchema,
)

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/sign-up", status_code=201, response_model=CustomerResponseSchema)
def sign_up(
    payload: CustomerSignUpRequestSchema,
    controller: CustomerSignUpController = Depends(get_sign_up_customer_controller),
):
    customer_data = CustomerSignUpDTO(payload.name, payload.email)
    return controller.execute(customer_data)


@router.post("/identify", status_code=201, response_model=CustomerResponseSchema)
def identify_by_cpf(
    payload: CustomerIdentifyByCPFRequestSchema,
    controller: CustomerIdentifyController = Depends(get_identify_customer_controller),
):
    customer_data = CustomerIdentifyDTO(payload.cpf)
    return controller.execute(customer_data)
