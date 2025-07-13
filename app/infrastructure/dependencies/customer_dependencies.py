from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.controllers.customer_identify_controller import CustomerIdentifyController
from app.adapters.controllers.customer_sign_up_controller import CustomerSignUpController
from app.adapters.gateways.customer_repository_gateway import CustomerRepositoryGateway
from app.adapters.presenters.customer_presenter import CustomerPresenter
from app.application.use_cases.customers.identify_customer import IdentifyCustomerUseCase
from app.application.use_cases.customers.sign_up_customer import SignUpCustomerUseCase
from app.config.database import get_database_session
from app.infrastructure.persistence.repositories.customer_repository import CustomerRepository


def get_customer_repository(
    session: Session = Depends(get_database_session)
) -> CustomerRepository:
    return CustomerRepository(session)


def get_customer_repository_gateway(
    repository: CustomerRepository = Depends(get_customer_repository)
) -> CustomerRepositoryGateway:
    return CustomerRepositoryGateway(repository)


def get_sign_up_customer_use_case(
    customer_repository_gateway: CustomerRepositoryGateway = Depends(get_customer_repository_gateway)
) -> SignUpCustomerUseCase:
    return SignUpCustomerUseCase(customer_repository_gateway)


def get_identify_customer_use_case(
    customer_repository_gateway: CustomerRepositoryGateway = Depends(get_customer_repository_gateway)
) -> IdentifyCustomerUseCase:
    return IdentifyCustomerUseCase(customer_repository_gateway)


def get_sign_up_customer_controller(
    use_case: SignUpCustomerUseCase = Depends(get_sign_up_customer_use_case)
) -> CustomerSignUpController:
    presenter = CustomerPresenter()
    return CustomerSignUpController(use_case, presenter)


def get_identify_customer_controller(
    use_case: IdentifyCustomerUseCase = Depends(get_identify_customer_use_case)
) -> CustomerIdentifyController:
    presenter = CustomerPresenter()
    return CustomerIdentifyController(use_case, presenter)
