from fastapi import APIRouter, Depends

from app.adapters.api.dtos.payment_dto import CreatePixPaymentRequestDTO, PaymentResponse, PixPaymentResponseDTO
from app.config.dependencies import get_create_payment_service
from app.application.services.create_payment_service import CreatePixPaymentService
from app.config.db import get_db

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post("/pix", response_model=PixPaymentResponseDTO)
def create_pix_payment(
    payment_data: CreatePixPaymentRequestDTO,
    service: CreatePixPaymentService = Depends(get_create_payment_service),
):
    result = service.execute(payment_data.dict())
    return PixPaymentResponseDTO(**result)


# @router.get("/{payment_id}", response_model=PaymentResponse)
# async def get_payment_status(
#     payment_id: str,
#     service: CreatePixPaymentService = Depends(get_create_payment_service),
# ):
#     result = service.get_payment_status(payment_id)
#     return PaymentResponse(**result)
