from sqlalchemy.orm import Session
from app.adapters.persistence.models.product import ProductModel
from app.domain.models.product import Product
from app.application.ports.product_port import ProductRepositoryPort

class ProductRepository(ProductRepositoryPort):
    def __init__(self, db, Session):
        self.db = db

    def listar_por_categoria(self, category, skip = 0, limit = 10):
        results = self.db.query(ProductModel)\
                            .filter_by(category=category)\
                            .offset(skip)\
                            .limit(limit)\
                            .all()
        return [Product(p.name, p.description, p.price, p.category) for p in results]
