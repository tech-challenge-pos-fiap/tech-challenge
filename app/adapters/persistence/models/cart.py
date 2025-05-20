import enum
from typing import List
from sqlalchemy import Column, Integer, Table, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import TimestampMixin


ProductCartModel = Table(
    'product_order',
    TimestampMixin.metadata,
    Column('product_id', ForeignKey('product.id'), primary_key=True),
    Column('cart_id', ForeignKey('cart.id'), primary_key=True),
    Column('quantity', Integer, nullable=False),
    Column('selected', Boolean, nullable=False),
)


class CartModel(TimestampMixin):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, index=True)
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel",
        secondary=ProductCartModel,
        back_populates="carts",
    )
