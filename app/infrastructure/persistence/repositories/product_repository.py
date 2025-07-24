from sqlalchemy.orm import Session

from app.adapters.gateways.repositories.mappers.product_mapper import ProductMapper
from app.adapters.gateways.repositories.product_repository_port import ProductRepositoryPort
from app.infrastructure.persistence.models.product import ProductModel


class ProductRepository(ProductRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def _mapper_to_model(self, product: ProductMapper) -> ProductModel:
        return ProductModel(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            image_path=product.image_path
        )

    def _model_to_mapper(self, instance: ProductMapper) -> ProductMapper:
        return ProductMapper(
            id=instance.id,
            name=instance.name,
            description=instance.description,
            price=instance.price,
            category=instance.category,
            image_path=instance.image_path
        )

    def save(self, product: ProductMapper) -> ProductMapper:
        instance = self._mapper_to_model(product)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return self._model_to_mapper(instance)

    def list_by_category(self, category: str, skip: int = 0, limit: int = 10) -> list[ProductMapper]:
        instances = self.session.query(ProductModel).filter_by(category=category).offset(skip).limit(limit).all()
        return [self._model_to_mapper(instance) for instance in instances]

    def filter(self, **kwargs) -> list[ProductMapper]:
        if not kwargs:
            instances = self.session.query(ProductModel).all()
            return [self._model_to_mapper(instance) for instance in instances]

        valid_types = (str, int, float, list, type(None))
        if not all(isinstance(v, valid_types) for v in kwargs.values()):
            raise ValueError("All filter values must be str, int, float, or list.")

        valid_keys = set(ProductModel.__table__.columns.keys())
        if not all(key in valid_keys for key in kwargs):
            raise ValueError("Invalid filter keys provided.")

        singular_kwargs = {k: v for k, v in kwargs.items() if not isinstance(v, list)}
        list_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, list)}

        instances = self.session.query(ProductModel).filter_by(**singular_kwargs)
        for key, value in list_kwargs.items():
            instances = instances.filter(getattr(ProductModel, key).in_(value))

        return [self._model_to_mapper(instance) for instance in instances]

    def update(self, product_id: int, product: ProductMapper) -> ProductMapper:
        instance = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not instance:
            return None

        for key, value in product.__dict__.items():
            if value is not None:
                setattr(instance, key, value)

        self.session.commit()
        self.session.refresh(instance)
        return self._model_to_mapper(instance)

    def delete(self, product_id: int) -> bool:
        instance = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True
