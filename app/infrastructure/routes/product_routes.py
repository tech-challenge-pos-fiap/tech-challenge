from typing import List

from fastapi import APIRouter, Depends

from app.adapters.controllers.products.create_product_controller import CreateProductController
from app.adapters.controllers.products.delete_product_controller import DeleteProductController
from app.adapters.controllers.products.list_products_by_category_controller import ListProductsByCategoryController
from app.adapters.controllers.products.update_product_controller import UpdateProductController
from app.infrastructure.dependencies.product_dependencies import (
    get_create_product_controller,
    get_delete_product_controller,
    get_list_products_by_category_controller,
    get_update_product_controller,
)
from app.infrastructure.routes.schemas.product_schemas import CreateProductSchema, ProductResponseSchema

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{category}", response_model=List[ProductResponseSchema])
def list_products_by_category(
    category: str,
    skip: int = 0,
    limit: int = 10,
    controller: ListProductsByCategoryController = Depends(get_list_products_by_category_controller)
):
    return controller.execute(category, skip, limit)


@router.post("/", response_model=ProductResponseSchema, status_code=201)
def create_product(
    product: CreateProductSchema,
    controller: CreateProductController = Depends(get_create_product_controller)
):
    return controller.execute(product)


@router.put("/{product_id}", response_model=ProductResponseSchema)
def update_product(
    product_id: int,
    product: CreateProductSchema,
    controller: UpdateProductController = Depends(get_update_product_controller)
):
    return controller.execute(product_id, product)


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    controller: DeleteProductController = Depends(get_delete_product_controller)
):
    return controller.execute(product_id)
