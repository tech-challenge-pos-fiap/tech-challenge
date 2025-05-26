from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.adapters.api.dtos.order_dto import WriteOrderDTO
from app.adapters.persistence.repositories.order_repository import OrderRepository
from app.application.services.orders.create_order_service import CreateOrderService
from app.application.services.orders.get_all_order_service import GetAllOrderService
from app.application.services.orders.get_order_service import GetOrderService
from app.application.services.orders.update_order_service import UpdateOrderService
from app.config.dependencies import (
    get_create_order_service,
    get_get_all_order_service,
    get_get_order_service,
    get_update_order_service
)
from app.config.db import get_db

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])
@router.post("/")
def create_order(order: WriteOrderDTO, service: CreateOrderService = Depends(get_create_order_service)):
    return service.execute(order.dict())

@router.get("/{order_id}")
def get_order(order_id: int, service: GetOrderService = Depends(get_get_order_service)):
    return service.execute(order_id)

@router.get("/")
def get_all_orders(skip: int = 0, limit: int = 10, service: GetAllOrderService = Depends(get_get_all_order_service)):
    return service.execute(skip, limit)

@router.put("/{order_id}")
def update_order(order_id: int, order: WriteOrderDTO, service: UpdateOrderService = Depends(get_update_order_service)):
    return service.execute(order_id, order.dict())
