import enum

from sqlalchemy import Column, Enum, Float, Integer, String

from .base import TimestampMixin


class ProductCategory(str, enum.Enum):
    BURGUERS = 'burguers'
    DRINKS = 'drinks'
    APPETIZERS = 'appetizers'
    DESSERTS = 'desserts'


class ProductModel(TimestampMixin):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Enum(ProductCategory, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    image_path = Column(String(255), nullable=True)
