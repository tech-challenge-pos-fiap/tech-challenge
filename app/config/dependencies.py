from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.persistence.repositories.customer_repository import CustomerRepository
from app.adapters.persistence.repositories.product_repository import ProductRepository
from app.application.services.create_products_service import CreateProductsService
from app.application.services.delete_products import DeleteProductsService
from app.application.services.identify_customer_service import IdentifyCustomerService
from app.application.services.list_products_service import ListProductsService
from app.application.services.sign_up_customer_service import SignUpCustomerService
from app.application.services.update_products_service import UpdateProductsService
from app.config.db import get_db


def get_sign_up_service(db: Session = Depends(get_db)) -> SignUpCustomerService:
    repository = CustomerRepository(db)
    return SignUpCustomerService(repository)


def get_identify_by_cpf_service(db: Session = Depends(get_db)) -> IdentifyCustomerService:
    repository = CustomerRepository(db)
    return IdentifyCustomerService(repository)


def get_list_products_service(db: Session = Depends(get_db)) -> ListProductsService:
    repository = ProductRepository(db)
    return ListProductsService(repository)


def get_create_products_service(db: Session = Depends(get_db)) -> CreateProductsService:
    repository = ProductRepository(db)
    return CreateProductsService(repository)


def get_update_products_service(db: Session = Depends(get_db)) -> UpdateProductsService:
    repository = ProductRepository(db)
    return UpdateProductsService(repository)


def get_delete_products_service(db: Session = Depends(get_db)) -> DeleteProductsService:
    repository = ProductRepository(db)
    return DeleteProductsService(repository)
