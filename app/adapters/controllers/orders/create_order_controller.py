from app.adapters.presenters.order_presenter import OrderPresenter
from app.application.use_cases.orders.create_order import CreateOrderUseCase


class CreateOrderController:
    def __init__(self, use_case: CreateOrderUseCase, presenter: OrderPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, order_data):
        order = self.use_case.execute(order_data)
        return self.presenter.present(order)
