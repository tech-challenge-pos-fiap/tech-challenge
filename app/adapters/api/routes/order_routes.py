from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.adapters.api.dtos.order_dto import OrderDTO
from app.adapters.persistence.repositories.order_repository import OrderRepository
from app.application.services.orders.create_order_service import CreateOrderService
from app.config.db import get_db

router = APIRouter()
@router.post("/orders", response_model=OrderDTO)
def create_order(order: OrderDTO, db: Session = Depends(get_db)):
    repo = OrderRepository(db)
    service = CreateOrderService(repo)
    return service.execute(order.dict())
