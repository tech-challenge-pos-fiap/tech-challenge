from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.db import get_db
from app.adapters.persistence.repositories.customer_repository import CustomerRepository
from app.application.services.sign_up_customer_service import SignUpCustomerService
from app.application.services.identify_customer_service import IdentifyCustomerService


def get_sign_up_service(db: Session = Depends(get_db)) -> SignUpCustomerService:
    repository = CustomerRepository(db)
    return SignUpCustomerService(repository)


def get_identify_by_cpf_service(db: Session = Depends(get_db)) -> IdentifyCustomerService:
    repo = CustomerRepository(db)
    return IdentifyCustomerService(repo)
