from fastapi import APIRouter, Depends

from app.adapters.controllers.dtos.order_dtos import UpdateOrderStatusDTO
from app.adapters.controllers.orders.checkout_order_controller import create_checkout_order_endpoint
from app.adapters.controllers.orders.create_order_controller import CreateOrderController
from app.adapters.controllers.orders.get_all_orders_controller import GetAllOrdersController
from app.adapters.controllers.orders.get_order_by_id_controller import GetOrderByIdController
from app.adapters.controllers.orders.update_order_status_controller import update_status_endpoint
from app.application.use_cases.orders.checkout_order import CheckoutOrder
from app.application.use_cases.orders.update_order_status import UpdateOrderStatus
from app.infrastructure.dependencies.order_dependencies import (
    get_checkout_order_use_case,
    get_create_order_controller,
    get_get_all_orders_controller,
    get_get_order_by_id_controller,
    get_update_order_status_use_case,
)
from app.infrastructure.routes.schemas.order_schemas import (
    CreateOrderRequestSchema,
    OrderSchema,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderSchema])
def get_all_orders(
    skip: int = 0,
    limit: int = 10,
    controller: GetAllOrdersController = Depends(get_get_all_orders_controller),
):
    response = controller.execute(skip, limit)
    return response


@router.post("/", response_model=OrderSchema, status_code=201)
def create_order(
    payload: CreateOrderRequestSchema,
    controller: CreateOrderController = Depends(get_create_order_controller),
):
    return controller.execute(payload.model_dump())


@router.get("/{order_id}", response_model=OrderSchema)
def get_order_by_id(
    order_id: int,
    controller: GetOrderByIdController = Depends(get_get_order_by_id_controller),
):
    return controller.execute(order_id)

@router.post("/checkout", response_model=OrderSchema)
def checkout_order(
    order: CreateOrderRequestSchema,
    use_case: CheckoutOrder = Depends(get_checkout_order_use_case)
):
    return create_checkout_order_endpoint(order, use_case)

@router.put("/{order_id}/status", response_model=OrderSchema)
def update_order_status(
    order_id: int,
    dto: UpdateOrderStatusDTO,
    use_case: UpdateOrderStatus = Depends(get_update_order_status_use_case)
):
    return update_status_endpoint(order_id, dto, use_case)
