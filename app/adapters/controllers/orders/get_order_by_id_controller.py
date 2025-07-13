from app.adapters.presenters.order_presenter import OrderPresenter
from app.application.use_cases.orders.get_order_by_id import GetOrderByIdUseCase


class GetOrderByIdController:
    def __init__(self, use_case: GetOrderByIdUseCase, presenter: OrderPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, order_id):
        order = self.use_case.execute(order_id)
        return self.presenter.present(order)
