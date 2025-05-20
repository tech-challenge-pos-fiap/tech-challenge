from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.adapters.persistence.repositories.product_repository import ProductRepository
from app.application.services.list_products import ListProductsService
from app.adapters.api.dtos.product_dto import ProductDTO
from typing import List

router = APIRouter()


@router.get("/products/category/{category}", response_model=List[ProductDTO])
def listar_por_categoria(categoy: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    service = ListProductsService(repo)
    return service.executar(categoy, skip, limit)