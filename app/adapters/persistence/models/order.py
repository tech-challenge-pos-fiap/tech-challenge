import enum
from typing import List, Optional

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship

from .base import TimestampMixin


class OrderStatus(enum.Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class OrderItemModel(TimestampMixin):
    __tablename__ = 'order_item'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product: Mapped[Optional["ProductModel"]] = relationship("ProductModel", back_populates="orders")
    quantity = Column(Integer, nullable=False)

class OrderModel(TimestampMixin):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel",
        secondary=OrderItemModel,
        back_populates="orders",
    )
    status = Column(Enum(OrderStatus), nullable=False)
    total_price = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    customer: Mapped[Optional["CustomerModel"]] = relationship("CustomerModel", back_populates="orders")
