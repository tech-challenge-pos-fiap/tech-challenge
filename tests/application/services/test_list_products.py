from app.application.use_cases.products.list_products_by_category import ProductRepositoryGatewayPort
from app.domain.entities.product import Product


class ProdutoRepoFake:
    def list_by_category(self, categoria, skip=0, limit=10):
        return [Product(1, 'X-Teste', 'Descrição teste', 10.0, categoria, None)]


def test_list_products():
    repo_fake = ProdutoRepoFake()
    service = ProductRepositoryGatewayPort(repo_fake)
    produtos = service.execute('lanche')

    assert len(produtos) == 1
    assert produtos[0].name == 'X-Teste'
