from app.application.ports.produto_port import ProdutoRepositoryPort
from app.domain.models.produto import Produto
from typing import List

class ListarProdutosService:
    def __init__(self, produto_repo: ProdutoRepositoryPort):
        self.repo = produto_repo
    
    def executar(self, categoria: str, skip: int = 0, limit: int = 10) -> List[Produto]:
        return self.repo.listar_por_categoria(categoria, skip, limit)