from app.adapters.controllers.dtos.order_dtos import UpdateOrderStatusDTO
from app.adapters.presenters.order_presenter import OrderPresenter
from app.application.use_cases.orders.update_order_status import UpdateOrderStatusUseCase
from app.domain.entities.order import Order


class UpdateOrderStatusController:
    def __init__(self, use_case: UpdateOrderStatusUseCase, presenter: OrderPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, order_id: int, payload: UpdateOrderStatusDTO) -> Order:
        order = self.use_case.execute(order_id, payload.status)
        return self.presenter.present(order)
