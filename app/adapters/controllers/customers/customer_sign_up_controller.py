from app.adapters.controllers.dtos.customer_dtos import CustomerSignUpDTO
from app.adapters.presenters.customer_presenter import CustomerPresenter
from app.application.use_cases.customers.sign_up_customer import SignUpCustomerUseCase


class CustomerSignUpController:
    def __init__(self, use_case: SignUpCustomerUseCase, presenter: CustomerPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, customer_data: CustomerSignUpDTO):
        customer = self.use_case.execute(customer_data.name, customer_data.email)
        return self.presenter.present(customer)
