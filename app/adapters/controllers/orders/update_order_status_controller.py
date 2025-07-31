from app.application.use_cases.orders.update_order_status import UpdateOrderStatus
from app.domain.dtos.update_order_status_dto import UpdateOrderStatusDTO
from app.domain.models.order import Order

def update_order_status_controller(
    order_id: int,
    dto: UpdateOrderStatusDTO,
    use_case: UpdateOrderStatus,
) -> Order:
    return use_case.execute(order_id, dto.status)