from app.application.services.listar_produtos import ListarProdutosService
from app.domain.models.produto import Produto

class ProdutoRepoFake:
    def listar_por_categoria(self, categoria, skip=0, limit=10):
        return [Produto("X-Teste", "Descrição teste", 10.0, categoria)]

def test_listar_produtos():
    repo_fake = ProdutoRepoFake()
    service = ListarProdutosService(repo_fake)
    produtos = service.executar("lanche")
    assert len(produtos) == 1
    assert produtos[0].nome == "X-Teste"
