from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.orders.checkout_order import CheckoutOrder
from app.config.database import get_database_session
from app.infrastructure.persistence.repositories.order_repository import OrderRepository


def get_checkout_order_use_case(db: Session = Depends(get_database_session)) -> CheckoutOrder:
    repository = OrderRepository(db)
    return CheckoutOrder(repository)
