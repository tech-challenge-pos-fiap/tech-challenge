from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.controllers.orders.create_order_controller import CreateOrderController
from app.adapters.controllers.orders.get_all_orders_controller import GetAllOrdersController
from app.adapters.controllers.orders.get_order_by_id_controller import GetOrderByIdController
from app.adapters.gateways.order_repository_gateway import OrderRepositoryGateway
from app.adapters.presenters.order_presenter import OrderPresenter
from app.application.use_cases.orders.create_order import CreateOrderUseCase
from app.application.use_cases.orders.get_all_orders import GetAllOrdersUseCase
from app.application.use_cases.orders.get_order_by_id import GetOrderByIdUseCase
from app.config.database import get_database_session
from app.infrastructure.persistence.repositories.order_repository import OrderRepository


def get_order_repository(session: Session = Depends(get_database_session)) -> OrderRepository:
    return OrderRepository(session)


def get_order_repository_gateway(
    repository: OrderRepository = Depends(get_order_repository),
) -> OrderRepositoryGateway:
    return OrderRepositoryGateway(repository)


def get_get_all_orders_use_case(
    order_repository_gateway: OrderRepositoryGateway = Depends(get_order_repository_gateway),
) -> GetAllOrdersUseCase:
    return GetAllOrdersUseCase(order_repository_gateway)


def get_create_order_use_case(
    order_repository_gateway: OrderRepositoryGateway = Depends(get_order_repository_gateway),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(order_repository_gateway)


def get_get_order_by_id_use_case(
    order_repository_gateway: OrderRepositoryGateway = Depends(get_order_repository_gateway),
) -> GetOrderByIdUseCase:
    return GetOrderByIdUseCase(order_repository_gateway)


def get_get_all_orders_controller(
    use_case: GetAllOrdersUseCase = Depends(get_get_all_orders_use_case),
) -> GetAllOrdersController:
    presenter = OrderPresenter()
    return GetAllOrdersController(use_case, presenter)


def get_create_order_controller(
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
) -> CreateOrderController:
    presenter = OrderPresenter()
    return CreateOrderController(use_case, presenter)


def get_get_order_by_id_controller(
    use_case: GetOrderByIdUseCase = Depends(get_get_order_by_id_use_case),
) -> GetOrderByIdController:
    presenter = OrderPresenter()
    return GetOrderByIdController(use_case, presenter)
