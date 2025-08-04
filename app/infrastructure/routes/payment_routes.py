from fastapi import APIRouter, Depends, HTTPException

from app.adapters.controllers.payments.get_payment_by_id_controller import GetPaymentByIdController
from app.adapters.controllers.payments.get_payments_by_order_id_controller import GetPaymentsByOrderIdController
from app.adapters.controllers.payments.process_payment_controller import ProcessPaymentController
from app.adapters.controllers.payments.webhook_payment_controller import WebhookPaymentController
from app.infrastructure.dependencies.payment_dependencies import (
    get_get_payment_by_id_controller,
    get_get_payments_by_order_id_controller,
    get_process_payment_controller,
    get_webhook_payment_controller,
)
from app.infrastructure.routes.schemas.payment_schemas import (
    PaymentResponse,
    ProcessPaymentRequest,
    WebhookData,
    WebhookResponse,
)

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/process-payment", status_code=201, response_model=PaymentResponse)
def process_payment(
    payment_data: ProcessPaymentRequest,
    controller: ProcessPaymentController = Depends(get_process_payment_controller),
):
    try:
        response = controller.execute(payment_data.model_dump())
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/webhook", status_code=200, response_model=WebhookResponse)
def webhook_payment(
    webhook_data: WebhookData,
    controller: WebhookPaymentController = Depends(get_webhook_payment_controller),
):
    """Webhook endpoint to receive payment status updates from Mercado Pago"""
    response = controller.execute(webhook_data.model_dump())
    return response


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment_by_id(
    payment_id: int,
    controller: GetPaymentByIdController = Depends(get_get_payment_by_id_controller),
):
    try:
        return controller.execute(payment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/order/{order_id}", response_model=list[PaymentResponse])
def get_payments_by_order_id(
    order_id: int,
    controller: GetPaymentsByOrderIdController = Depends(get_get_payments_by_order_id_controller),
):
    return controller.execute(order_id)
