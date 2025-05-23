from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.adapters.api.dtos.product_dto import Product, ProductResponse
from app.adapters.api.dtos.response_dto import ResponseModel
from app.application.services.create_products_service import CreateProductsService
from app.application.services.delete_products import DeleteProductsService
from app.application.services.list_products_service import ListProductsService
from app.application.services.update_products_service import UpdateProductsService
from app.config.dependencies import (
    get_create_products_service,
    get_delete_products_service,
    get_list_products_service,
    get_update_products_service,
)

router = APIRouter(prefix='/products', tags=['Products'])


@router.get('/category/{category}', response_model=List[ProductResponse])
def list_by_category(
        category: str,
        skip: int = 0,
        limit: int = 10,
        service: ListProductsService = Depends(get_list_products_service)
    ):

    return service.execute(category, skip, limit)


@router.post('', response_model=ResponseModel[ProductResponse], status_code=201)
def create_product(
        product: Product,
        service: CreateProductsService = Depends(get_create_products_service)
    ):

    product = service.execute(product)

    return ResponseModel(
        message='Produto criado com sucesso.',
        data=ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category
        )
    )

@router.put('/{id}', response_model=ResponseModel[ProductResponse], status_code=200)
def update_product(
        id: int,
        product: Product,
        service: UpdateProductsService = Depends(get_update_products_service)
    ):

    product = service.execute(id, product)

    return ResponseModel(
        message='Produto atualizado com sucesso.',
        data=ProductResponse(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category
        )
    )

@router.delete('/{id}', response_model=ResponseModel[None], status_code=200)
def delete_product(
        id: int,
        service: DeleteProductsService = Depends(get_delete_products_service)
    ):

    deleted = service.execute(id)

    if not deleted:
        raise HTTPException(status_code=404, detail='Produto não encontrado.')

    return ResponseModel(
        message='Produto deletado com sucesso.'
    )
