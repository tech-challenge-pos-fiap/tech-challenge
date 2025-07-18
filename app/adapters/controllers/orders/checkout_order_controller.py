from fastapi import Depends
from app.adapters.controllers.dtos.order_dtos import CheckoutOrderDTO
from app.application.use_cases.orders.checkout_order import CheckoutOrder
from app.infrastructure.dependencies import get_checkout_order_use_case

def create_checkout_order_endpoint(
    order: CheckoutOrderDTO,
    use_case: CheckoutOrder = Depends(get_checkout_order_use_case)
):
    return use_case.execute(order.dict())
