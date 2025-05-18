import enum
from sqlalchemy import Column, Integer, String, Float, Enum
from .base import TimestampMixin

class ProductCategory(enum.Enum):
    burguers = 1
    drinks = 2
    appetizers = 3
    desserts = 4

class ProductModel(TimestampMixin):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
