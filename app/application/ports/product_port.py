# app/application/ports/produto_port.py
from abc import ABC, abstractmethod

class ProdutoRepositoryPort(ABC):
    @abstractmethod
    def listar_por_categoria(self, category: str, skip: int = 0, limit: int = 10):
        pass
