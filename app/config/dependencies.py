from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.external.mercado_pago.payment_service import MercadoPagoPaymentService
from app.adapters.external.mercado_pago.pix import MercadoPagoPixClient
from app.adapters.persistence.repositories.customer_repository import CustomerRepository
from app.adapters.persistence.repositories.order_repository import OrderRepository
from app.adapters.persistence.repositories.payment_repository import PaymentRepository
from app.adapters.persistence.repositories.product_repository import ProductRepository
from app.application.services.create_payment_service import CreatePixPaymentService
from app.application.services.create_products_service import CreateProductsService
from app.application.services.delete_products import DeleteProductsService
from app.application.services.identify_customer_service import IdentifyCustomerService
from app.application.services.list_payment_service import ListPaymentService
from app.application.services.list_products_service import ListProductsService
from app.application.services.orders.create_order_service import CreateOrderService
from app.application.services.orders.get_all_order_service import GetAllOrderService
from app.application.services.orders.get_order_service import GetOrderService
from app.application.services.orders.update_order_service import UpdateOrderService
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

def get_create_payment_service(db: Session = Depends(get_db)) -> CreatePixPaymentService:
    client = MercadoPagoPixClient()
    payment_adapter = MercadoPagoPaymentService(client, db)
    order_repository = OrderRepository(db)
    return CreatePixPaymentService(payment_adapter, order_repository)

def get_get_payment_service(db: Session = Depends(get_db)) -> ListPaymentService:
    repository = PaymentRepository(db)
    return ListPaymentService(repository)

def get_get_payment_service_by_order_id(db: Session = Depends(get_db)) -> ListPaymentService:
    repository = PaymentRepository(db)
    return ListPaymentService(repository)

def get_create_order_service(db: Session = Depends(get_db)) -> CreateOrderService:
    repository = OrderRepository(db)
    return CreateOrderService(repository)

def get_get_all_order_service(db: Session = Depends(get_db)) -> GetAllOrderService:
    repository = OrderRepository(db)
    return GetAllOrderService(repository)

def get_get_order_service(db: Session = Depends(get_db)) -> GetOrderService:
    repository = OrderRepository(db)
    return GetOrderService(repository)

def get_update_order_service(db: Session = Depends(get_db)) -> UpdateOrderService:
    repository = OrderRepository(db)
    return UpdateOrderService(repository)
