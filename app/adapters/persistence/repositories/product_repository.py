from sqlalchemy.orm import Session

from app.adapters.persistence.models.product import ProductModel
from app.application.ports.product_repository_port import ProductRepositoryPort
from app.domain.models.product import Product


class ProductRepository(ProductRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def list_by_category(self, category, skip=0, limit=10):
        results = self.db.query(ProductModel)\
            .filter_by(category=category)\
            .offset(skip)\
            .limit(limit)\
            .all()
        return [Product(p.name, p.description, p.price, p.category) for p in results]
