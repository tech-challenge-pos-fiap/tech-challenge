from app.application.services.list_payment_service import ListPaymentService
from fastapi import APIRouter, Depends

from app.adapters.api.dtos.payment_dto import CreatePixPaymentRequest, PaymentResponse, PixPaymentResponse
from app.config.dependencies import get_create_payment_service, get_list_payment_service
from app.application.services.create_payment_service import CreatePixPaymentService
from app.config.db import get_db

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post("/pix", response_model=PixPaymentResponse)
def create_pix_payment(
    payment_data: CreatePixPaymentRequest,
    service: CreatePixPaymentService = Depends(get_create_payment_service),
):
    result = service.execute(payment_data.dict())
    return PixPaymentResponse(**result)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: str,
    service: ListPaymentService = Depends(get_list_payment_service),
):
    result = service.execute(payment_id)
    return PaymentResponse.from_orm(result)
