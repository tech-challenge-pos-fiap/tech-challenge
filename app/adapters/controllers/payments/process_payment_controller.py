from app.adapters.presenters.payment_presenter import PaymentPresenter
from app.application.use_cases.payments.process_payment import ProcessPaymentUseCase


class ProcessPaymentController:
    def __init__(self, use_case: ProcessPaymentUseCase, presenter: PaymentPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, payment_data: dict) -> dict:
        payment = self.use_case.execute(payment_data)
        return self.presenter.present(payment)
