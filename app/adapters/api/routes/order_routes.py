from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.adapters.api.dtos.order_dto import OrderDTO
from app.adapters.persistence.repositories.order_repository import OrderRepository
from app.application.services.orders.create_order_service import CreateOrderService
from app.application.services.orders.get_all_order_service import GetAllOrderService
from app.application.services.orders.get_order_service import GetOrderService
from app.application.services.orders.update_order_service import UpdateOrderService
from app.config.db import get_db

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])
@router.post("/", response_model=OrderDTO)
def create_order(order: OrderDTO, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = CreateOrderService(repo)
    return service.execute(order.dict())

@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = GetOrderService(repo)
    return service.execute(order_id)

@router.get("/")
def get_all_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = GetAllOrderService(repo)
    return service.execute(skip, limit)

@router.put("/{order_id}")
def update_order(order_id: int, order: OrderDTO, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = UpdateOrderService(repo)
    return service.execute(order_id, order.dict())
