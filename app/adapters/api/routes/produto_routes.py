from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.db import get_db
from app.adapters.persistence.repositories.produto_repository import ProdutoRepository
from app.application.services.listar_produtos import ListarProdutosService
from app.adapters.api.dtos.produto_dto import ProdutoDTO
from typing import List

router = APIRouter()


@router.get("/produtos/categoria/{categoria}", response_model=List[ProdutoDTO])
def listar_por_categoria(categoria: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    repo = ProdutoRepository(db)
    service = ListarProdutosService(repo)
    return service.executar(categoria, skip, limit)