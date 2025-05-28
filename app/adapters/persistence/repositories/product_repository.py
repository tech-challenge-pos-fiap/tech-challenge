from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.adapters.persistence.models.product import ProductModel
from app.application.ports.product_repository_port import ProductRepositoryPort
from app.domain.models.product import Product


class ProductRepository(ProductRepositoryPort):
    def __init__(self, db: Session):
        self.db = db


    def _to_domain(self, model: ProductModel) -> Product:
        return ProductModel(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            category=model.category,
            image_path=model.image_path
        )


    def list_by_category(self, category, skip=0, limit=10):
        results = self.db.query(ProductModel)\
            .filter_by(category=category)\
            .offset(skip)\
            .limit(limit)\
            .all()
        return [self._to_domain(p) for p in results]

    def save(self, product: Product):
        product_model = ProductModel(
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category
        )

        self.db.add(product_model)
        self.db.commit()
        self.db.refresh(product_model)

        return self._to_domain(product_model)

    def update(self, id: int, product: Product):
        product_model = self.db.query(ProductModel).filter_by(id=id).first()

        if not product_model:
            raise NoResultFound(f"Produto com nome '{product.name}' não encontrado.")

        product_model.name = product.name
        product_model.description = product.description
        product_model.price = product.price
        product_model.category = product.category

        self.db.commit()
        self.db.refresh(product_model)

        return self._to_domain(product_model)

    def delete(self, id: int) -> bool:
        product = self.db.query(ProductModel).filter_by(id=id).first()
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False
