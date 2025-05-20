from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.adapters.api.dtos.payment_dto import CreatePixPaymentRequestDTO
from app.adapters.external.mercado_pago.factory import get_payment_service
from app.adapters.external.mercado_pago.payment_service import MercadoPagoPaymentService
from app.config.db import get_db

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post("/pix")
async def create_pix_payment(
    payment_data: CreatePixPaymentRequestDTO,
    payment_service: MercadoPagoPaymentService = Depends(get_payment_service),
    db: Session = Depends(get_db)
):
    return payment_service.create_pix_payment(payment_data.dict())


@router.get("/{payment_id}")
async def get_payment_status(
    payment_id: str,
    payment_service: MercadoPagoPaymentService = Depends(get_payment_service),
    db: Session = Depends(get_db)
):
    return payment_service.get_payment_status(payment_id)
