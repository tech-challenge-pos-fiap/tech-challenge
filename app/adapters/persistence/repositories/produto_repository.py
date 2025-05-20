from sqlalchemy.orm import Session
from app.adapters.persistence.models.product import ProductModel
from app.domain.models.produto import Produto
from app.application.ports.produto_port import ProdutoRepositoryPort

class ProdutoRepository(ProdutoRepositoryPort):
    def __init__(self, db, Session):
        self.db = db
    
    def listar_por_categoria(self, categoria, skip = 0, limit = 10):
        resultados = self.db.query(ProdutoModel)\
                            .filter_by(categoria=categoria)\
                            .offset(skip)\
                            .limit(limit)\
                            .all()
        return [Produto(p.nome, p.descricao, p.preco, p.categoria) for p in resultados]