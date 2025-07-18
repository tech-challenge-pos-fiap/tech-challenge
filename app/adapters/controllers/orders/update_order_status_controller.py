from fastapi import Depends
from app.adapters.controllers.dtos.order_dtos import UpdateOrderStatusDTO
from app.application.use_cases.orders.update_order_status import UpdateOrderStatus
from app.config.dependencies import get_update_order_status_use_case

def update_status_endpoint(
    order_id: int,
    dto: UpdateOrderStatusDTO,
    use_case: UpdateOrderStatus = Depends(get_update_order_status_use_case)
):
    return use_case.execute(order_id, dto.status)
