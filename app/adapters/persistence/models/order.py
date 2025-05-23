import enum
from typing import List, Optional
from sqlalchemy import Column, Integer, Float, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from .base import TimestampMixin

ProductOrderModel = Table(
    'product_order',
    TimestampMixin.metadata,
    Column('product_id', ForeignKey('product.id'), primary_key=True),
    Column('order_id', ForeignKey('orders.id'), primary_key=True),
    Column('quantity', Integer, nullable=False),
)

class OrderStatus(enum.Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

class OrderModel(TimestampMixin):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    products: Mapped[List["ProductModel"]] = relationship(
        "ProductModel",
        secondary=ProductOrderModel,
        back_populates="orders",
    )
    status = Column(Enum(OrderStatus), nullable=False)
    total_price = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    customer: Mapped[Optional["CustomerModel"]] = relationship("CustomerModel", back_populates="orders")
