from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.controllers.products.create_product_controller import CreateProductController
from app.adapters.controllers.products.delete_product_controller import DeleteProductController
from app.adapters.controllers.products.list_products_by_category_controller import ListProductsByCategoryController
from app.adapters.controllers.products.update_product_controller import UpdateProductController
from app.adapters.gateways.product_repository_gateway import ProductRepositoryGateway
from app.adapters.presenters.product_presenter import ProductPresenter
from app.application.use_cases.products.create_product import CreateProductUseCase
from app.application.use_cases.products.delete_product import DeleteProductUseCase
from app.application.use_cases.products.list_products_by_category import ListProductsByCategoryUseCase
from app.application.use_cases.products.update_product import UpdateProductUseCase
from app.config.database import get_database_session
from app.infrastructure.persistence.repositories.product_repository import ProductRepository


def get_product_repository(session: Session = Depends(get_database_session)):
    return ProductRepository(session)


def get_product_repository_gateway(
    repository: ProductRepository = Depends(get_product_repository),
):
    return ProductRepositoryGateway(repository)


def get_create_product_use_case(
    repository_gateway: ProductRepositoryGateway = Depends(get_product_repository_gateway),
):
    return CreateProductUseCase(repository_gateway)


def list_products_by_category_use_case(
    repository_gateway: ProductRepositoryGateway = Depends(get_product_repository_gateway),
):
    return ListProductsByCategoryUseCase(repository_gateway)


def get_update_product_use_case(
    repository_gateway: ProductRepositoryGateway = Depends(get_product_repository_gateway),
):
    return UpdateProductUseCase(repository_gateway)


def get_delete_product_use_case(
    repository_gateway: ProductRepositoryGateway = Depends(get_product_repository_gateway),
):
    return DeleteProductUseCase(repository_gateway)


def get_create_product_controller(
    use_case: CreateProductUseCase = Depends(get_create_product_use_case),
):
    presenter = ProductPresenter()
    return CreateProductController(use_case, presenter)


def get_list_products_by_category_controller(
    use_case: ListProductsByCategoryUseCase = Depends(list_products_by_category_use_case),
):
    presenter = ProductPresenter()
    return ListProductsByCategoryController(use_case, presenter)


def get_update_product_controller(
    use_case: UpdateProductUseCase = Depends(get_update_product_use_case),
):
    presenter = ProductPresenter()
    return UpdateProductController(use_case, presenter)


def get_delete_product_controller(
    use_case: DeleteProductUseCase = Depends(get_delete_product_use_case),
):
    return DeleteProductController(use_case)
