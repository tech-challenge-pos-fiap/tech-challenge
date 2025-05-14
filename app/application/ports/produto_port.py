from abc import ABC, abstractclassmethod
from typing import List
from app.domain.models.produto import Produto

class ProdutoRepositoryPort(ABC):
    @abstractmethod
    def listar_por_categoria(self, categoria: str, skip: int = 0, limit: int = 10) -> List(Produto):
        pass