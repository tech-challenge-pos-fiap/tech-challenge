from fastapi import APIRouter, Depends, HTTPException
from app.adapters.api.dtos.payment_dto import CreatePixPaymentRequestDTO, PixPaymentResponseDTO
from app.application.services.create_payment_service import CreatePixPaymentService as PaymentService
from app.config.use_cases.payment import get_payment_use_case as get_payment_service

router = APIRouter()

@router.post("/payments/pix", response_model=PixPaymentResponseDTO)
async def create_pix_payment(
    payment_data: CreatePixPaymentRequestDTO,
    payment_service: PaymentService = Depends(get_payment_service)
):
    return await payment_service.create_payment(payment_data.dict())

@router.get("/payments/pix/{payment_id}", response_model=PixPaymentResponseDTO)
async def get_payment_status(
    payment_id: int,
    payment_service: PaymentService = Depends(get_payment_service)
):
    try:
        return await payment_service.get_payment_status(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))