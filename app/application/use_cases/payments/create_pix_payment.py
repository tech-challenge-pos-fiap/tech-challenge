from typing import Any, Dict

from fastapi import HTTPException, status

from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.application.ports.payments.payment_service_gateway import PaymentServiceGatewayPort


class CreatePixPaymentUseCase:
    def __init__(self, payment_service: PaymentServiceGatewayPort, order_repository: OrderRepositoryGatewayPort):
        self.payment_service = payment_service
        self.order_repository = order_repository

    def execute(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        self._validate_order(payment_data)
        return self.payment_service.create_pix_payment(payment_data)

    def _validate_order(self, payment_data: Dict[str, Any]) -> None:
        order_id = payment_data.get("order_id")
        if order_id is not None:
            order = self.order_repository.get(order_id)
            if not order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ordem com ID {order_id} não encontrada"
                )
