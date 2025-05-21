from app.application.services.list_products import ListProductsService
from app.domain.models.product import Product


class ProdutoRepoFake:
    def list_by_category(self, categoria, skip=0, limit=10):
        return [Product("X-Teste", "Descrição teste", 10.0, categoria)]


def test_list_products():
    repo_fake = ProdutoRepoFake()
    service = ListProductsService(repo_fake)
    produtos = service.execute("lanche")
    assert len(produtos) == 1
    assert produtos[0].nome == "X-Teste"
