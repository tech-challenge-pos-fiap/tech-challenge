from app.application.ports.product_port import ProductRepositoryPort
from app.domain.models.product import Product
from typing import List

class ListProductsService:
    def __init__(self, product_repo: ProductRepositoryPort):
        self.repo = product_repo
    
    def executar(self, category: str, skip: int = 0, limit: int = 10) -> List[Product]:
        return self.repo.listar_por_categoria(category, skip, limit)