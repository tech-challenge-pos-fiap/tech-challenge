from app.adapters.presenters.payment_presenter import PaymentPresenter
from app.application.use_cases.payments.get_payments_by_order_id import GetPaymentsByOrderIdUseCase


class GetPaymentsByOrderIdController:
    def __init__(self, use_case: GetPaymentsByOrderIdUseCase, presenter: PaymentPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, order_id) -> list:
        payments = self.use_case.execute(order_id)
        return [self.presenter.present(payment) for payment in payments]
