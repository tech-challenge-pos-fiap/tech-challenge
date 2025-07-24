from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.controllers.orders.create_order_controller import CreateOrderController
from app.adapters.controllers.orders.get_all_orders_controller import GetAllOrdersController
from app.adapters.controllers.orders.get_order_by_id_controller import GetOrderByIdController
<<<<<<< HEAD
from app.adapters.gateways.order_repository_gateway import OrderRepositoryGateway, OrderRepositoryGatewayPort
=======
from app.adapters.gateways.customer_repository_gateway import CustomerRepositoryGateway
from app.adapters.gateways.order_repository_gateway import OrderRepositoryGateway
from app.adapters.gateways.product_repository_gateway import ProductRepositoryGateway
>>>>>>> 7f1f3754f6287f6d0df6ffc84bf26611f552e157
from app.adapters.presenters.order_presenter import OrderPresenter
from app.application.use_cases.orders.checkout_order import CheckoutOrder
from app.application.use_cases.orders.create_order import CreateOrderUseCase
from app.application.use_cases.orders.get_all_orders import GetAllOrdersUseCase
from app.application.use_cases.orders.get_order_by_id import GetOrderByIdUseCase
from app.application.use_cases.orders.update_order_status import UpdateOrderStatus
from app.config.database import get_database_session
from app.infrastructure.dependencies.customer_dependencies import get_customer_repository_gateway
from app.infrastructure.dependencies.product_dependencies import get_product_repository_gateway
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
    product_repository_gateway: ProductRepositoryGateway = Depends(get_product_repository_gateway),
    customer_repository_gateway: CustomerRepositoryGateway = Depends(get_customer_repository_gateway),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(
        order_repository=order_repository_gateway,
        product_repository=product_repository_gateway,
        customer_repository=customer_repository_gateway,
    )


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

def get_update_order_status_use_case(
    order_repository_gateway: OrderRepositoryGateway = Depends(get_order_repository_gateway),
) -> UpdateOrderStatus:
    return UpdateOrderStatus(order_repository_gateway)

def get_checkout_order_use_case(
    order_repository_gateway: OrderRepositoryGateway = Depends(get_order_repository_gateway),
) -> CheckoutOrder:
    return CheckoutOrder(order_repository_gateway)
