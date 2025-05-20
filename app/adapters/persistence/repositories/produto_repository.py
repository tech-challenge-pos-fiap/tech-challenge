from app.application.ports.produto_port import ProdutoRepositoryPort
from app.domain.models.produto import Produto
from app.persistence.models.produto import Produto


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