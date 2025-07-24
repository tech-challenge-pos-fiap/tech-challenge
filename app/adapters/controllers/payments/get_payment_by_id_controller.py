from app.adapters.presenters.payment_presenter import PaymentPresenter
from app.application.use_cases.payments.get_payment_by_id import GetPaymentByIdUseCase


class GetPaymentByIdController:
    def __init__(self, use_case: GetPaymentByIdUseCase, presenter: PaymentPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, payment_id):
        payment = self.use_case.execute(payment_id)
        return self.presenter.present(payment) if payment else None
