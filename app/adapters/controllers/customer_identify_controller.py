from app.adapters.controllers.dtos.customer_dtos import CustomerIdentifyDTO
from app.adapters.presenters.customer_presenter import CustomerPresenter
from app.application.use_cases.customers.identify_customer import IdentifyCustomerUseCase


class CustomerIdentifyController:
    def __init__(self, use_case: IdentifyCustomerUseCase, presenter: CustomerPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, customer_data: CustomerIdentifyDTO):
        customer = self.use_case.execute(customer_data.cpf)
        return self.presenter.present(customer)
