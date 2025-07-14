from fastapi import APIRouter, Depends

from app.adapters.controllers.orders.create_order_controller import CreateOrderController
from app.adapters.controllers.orders.get_all_orders_controller import GetAllOrdersController
from app.adapters.controllers.orders.get_order_by_id_controller import GetOrderByIdController
from app.infrastructure.dependencies.order_dependencies import (
    get_create_order_controller,
    get_get_all_orders_controller,
    get_get_order_by_id_controller,
)
from app.infrastructure.routes.schemas.order_schemas import (
    CreateOrderRequestSchema,
    GetAllOrdersRequestSchema,
    OrderResponseSchema,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderResponseSchema])
def get_all_orders(
    payload: GetAllOrdersRequestSchema,
    controller: GetAllOrdersController = Depends(get_get_all_orders_controller),
):
    return controller.execute(payload.skip, payload.limit)


@router.post("/", response_model=OrderResponseSchema, status_code=201)
def create_order(
    payload: CreateOrderRequestSchema,
    controller: CreateOrderController = Depends(get_create_order_controller),
):
    return controller.execute(payload)


@router.get("/{order_id}", response_model=OrderResponseSchema)
def get_order_by_id(
    order_id: int,
    controller: GetOrderByIdController = Depends(get_get_order_by_id_controller),
):
    return controller.execute(order_id)
