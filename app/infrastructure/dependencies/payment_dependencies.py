import os

from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.controllers.payments.get_payment_by_id_controller import GetPaymentByIdController
from app.adapters.controllers.payments.get_payments_by_order_id_controller import GetPaymentsByOrderIdController
from app.adapters.controllers.payments.process_payment_controller import ProcessPaymentController
from app.adapters.controllers.payments.webhook_payment_controller import WebhookPaymentController
from app.adapters.gateways.order_repository_gateway import OrderRepositoryGateway
from app.adapters.gateways.payment_repository_gateway import PaymentRepositoryGateway
from app.adapters.gateways.payment_service_gateway import PaymentServiceGateway
from app.adapters.presenters.payment_presenter import PaymentPresenter
from app.application.use_cases.payments.get_payment_by_id import GetPaymentByIdUseCase
from app.application.use_cases.payments.get_payments_by_order_id import GetPaymentsByOrderIdUseCase
from app.application.use_cases.payments.process_payment import ProcessPaymentUseCase
from app.application.use_cases.payments.update_payment_status import UpdatePaymentStatusUseCase
from app.config.database import get_database_session
from app.infrastructure.dependencies.order_dependencies import get_order_repository_gateway
from app.infrastructure.external.external_payment_service import ExternalPaymentProcessService
from app.infrastructure.external.mercado_pago_mock_service import MercadoPagoMockService
from app.infrastructure.persistence.repositories.payment_repository import PaymentRepository


def get_payment_repository(session: Session = Depends(get_database_session)) -> PaymentRepository:
    return PaymentRepository(session)


def get_payment_validation_service() -> ExternalPaymentProcessService:
    """Get payment validation service instance."""
    return ExternalPaymentProcessService()


def get_mercado_pago_service():
    """Get Mercado Pago service instance."""
    return MercadoPagoMockService(success_rate=0.9)


def get_payment_repository_gateway(
    repository: PaymentRepository = Depends(get_payment_repository),
) -> PaymentRepositoryGateway:
    return PaymentRepositoryGateway(repository)


def get_payment_service_gateway(
    validation_service: ExternalPaymentProcessService = Depends(get_payment_validation_service),
    mp_service=Depends(get_mercado_pago_service),
) -> PaymentServiceGateway:
    return PaymentServiceGateway(validation_service, mp_service)


def get_process_payment_use_case(
    payment_repository_gateway: PaymentRepositoryGateway = Depends(get_payment_repository_gateway),
    payment_service_gateway: PaymentServiceGateway = Depends(get_payment_service_gateway),
    order_repository_gateway: OrderRepositoryGateway = Depends(get_order_repository_gateway),
) -> ProcessPaymentUseCase:
    return ProcessPaymentUseCase(
        payment_repository=payment_repository_gateway,
        payment_service=payment_service_gateway,
        order_repository=order_repository_gateway,
    )


def get_update_payment_status_use_case(
    payment_repository_gateway: PaymentRepositoryGateway = Depends(get_payment_repository_gateway),
) -> UpdatePaymentStatusUseCase:
    return UpdatePaymentStatusUseCase(payment_repository=payment_repository_gateway)


def get_get_payment_by_id_use_case(
    payment_repository_gateway: PaymentRepositoryGateway = Depends(get_payment_repository_gateway),
) -> GetPaymentByIdUseCase:
    return GetPaymentByIdUseCase(payment_repository=payment_repository_gateway)


def get_get_payments_by_order_id_use_case(
    payment_repository_gateway: PaymentRepositoryGateway = Depends(get_payment_repository_gateway),
) -> GetPaymentsByOrderIdUseCase:
    return GetPaymentsByOrderIdUseCase(payment_repository=payment_repository_gateway)


def get_get_payment_by_id_controller(
    get_payment_by_id_use_case: GetPaymentByIdUseCase = Depends(get_get_payment_by_id_use_case),
) -> GetPaymentByIdController:
    presenter = PaymentPresenter()
    return GetPaymentByIdController(
        use_case=get_payment_by_id_use_case,
        presenter=presenter,
    )


def get_get_payments_by_order_id_controller(
    get_payments_by_order_id_use_case: GetPaymentsByOrderIdUseCase = Depends(get_get_payments_by_order_id_use_case),
) -> GetPaymentsByOrderIdController:
    presenter = PaymentPresenter()
    return GetPaymentsByOrderIdController(
        use_case=get_payments_by_order_id_use_case,
        presenter=presenter,
    )


def get_process_payment_controller(
    process_payment_use_case: ProcessPaymentUseCase = Depends(get_process_payment_use_case),
) -> ProcessPaymentController:
    presenter = PaymentPresenter()
    return ProcessPaymentController(
        use_case=process_payment_use_case,
        presenter=presenter,
    )


def get_webhook_payment_controller(
    update_payment_status_use_case: UpdatePaymentStatusUseCase = Depends(get_update_payment_status_use_case),
) -> WebhookPaymentController:
    return WebhookPaymentController(use_case=update_payment_status_use_case)
