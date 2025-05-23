import enum

from sqlalchemy import Column, Enum, Float, Integer, String
from sqlalchemy.orm import relationship

from .base import TimestampMixin


class ProductCategory(str, enum.Enum):
    BURGUERS = "burguers"
    DRINKS = "drinks"
    APPETIZERS = "appetizers"
    DESSERTS = "desserts"


class ProductModel(TimestampMixin):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(Enum(ProductCategory), nullable=False)
    orders = relationship(
        "OrderModel",
        secondary='product_order',
        back_populates="products",
    )
