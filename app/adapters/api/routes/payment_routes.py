from fastapi import APIRouter, Depends, HTTPException, status
from requests.exceptions import HTTPError, RequestException
from sqlalchemy.exc import NoResultFound

from app.adapters.api.dtos.payment_dto import CreatePixPaymentRequest, PaymentResponse, PixPaymentResponse
from app.application.services.create_payment_service import CreatePixPaymentService
from app.application.services.list_payment_service import ListPaymentService
from app.config.dependencies import (
    get_create_payment_service,
    get_get_payment_service,
    get_get_payment_service_by_order_id,
)

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/order/{order_id}", response_model=list[PaymentResponse])
def get_payments_by_order(
    order_id: int,
    service: ListPaymentService = Depends(get_get_payment_service_by_order_id),
):
    try:
        payments = service.get_payment_by_order_id(order_id)
        return [PaymentResponse.model_validate(p) for p in payments]
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no servidor - {e}"
        ) from e

@router.post("/pix", response_model=PixPaymentResponse)
def create_pix_payment(
    payment_data: CreatePixPaymentRequest,
    service: CreatePixPaymentService = Depends(get_create_payment_service),
):
    try:
        result = service.execute(payment_data.dict())
        return PixPaymentResponse(**result)

    except HTTPException as e:
        raise e

    except HTTPError as e:
        status_code = e.response.status_code if e.response else 502
        detail = e.response.json() if e.response else str(e)
        raise HTTPException(status_code=status_code, detail=detail) from e

    except RequestException as e:
        raise HTTPException(status_code=503, detail="Erro de comunicação com o Mercado Pago") from e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor - {e}") from e

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: str,
    service: ListPaymentService = Depends(get_get_payment_service),
):
    try:
        payment = service.get_payment_by_id(payment_id)
        return PaymentResponse.from_orm(payment)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor - {e}") from e
