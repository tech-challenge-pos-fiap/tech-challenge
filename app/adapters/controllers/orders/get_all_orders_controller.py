from app.adapters.presenters.order_presenter import OrderPresenter
from app.application.use_cases.orders.get_all_orders import GetAllOrdersUseCase


class GetAllOrdersController:
    def __init__(
        self,
        use_case: GetAllOrdersUseCase,
        presenter: OrderPresenter,
    ):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, skip: int = 0, limit: int = 10):
        orders = self.use_case.execute(skip, limit)
        return [self.presenter.present(order) for order in orders]
