import enum
from typing import List
from sqlalchemy import Column, Integer, Float, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import TimestampMixin


ProductOrderModel = Table(
    'product_order',
    TimestampMixin.metadata,
    Column('product_id', ForeignKey('product.id'), primary_key=True),
    Column('order_id', ForeignKey('order.id'), primary_key=True),
)


class OrderStatus(enum.Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'


class OrderModel(TimestampMixin):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, index=True)
    # client = Column(String, nullable=False) TODO - add client model
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel",
        secondary=ProductOrderModel,
        back_populates="orders",
    )
    status = Column(Enum(OrderStatus), nullable=False)
    total_price = Column(Float, nullable=False)
