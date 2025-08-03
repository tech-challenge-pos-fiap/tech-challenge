from enum import Enum
from typing import List, Optional

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.models.payment import PaymentModel
from app.infrastructure.persistence.models.product import ProductModel

from .base import Base, TimestampMixin



class OrderStatus(enum.Enum):
    PENDING = 'pending'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    RECEIVED = 'received'
    IN_PREPARATION = 'in_preparation'
    READY = 'ready'
    FINISHED = 'finished'


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="items")
    product: Mapped["ProductModel"] = relationship("ProductModel")



class OrderModel(TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    items: Mapped[List["OrderItemModel"]] = relationship(
        OrderItemModel,
        back_populates="order",
        cascade="all, delete-orphan",
    )
    status: Mapped[str] = mapped_column(
        SqlEnum(
            OrderStatus, name="orderstatus", native_enum=True, values_callable=lambda x: [e.value for e in OrderStatus]
        ),
        nullable=False,
        default="pending",
    )
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    customer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("customers.id"), nullable=True)

    customer: Mapped[Optional["CustomerModel"]] = relationship("CustomerModel", back_populates="orders")
    payments: Mapped[List["PaymentModel"]] = relationship(PaymentModel, back_populates="order")
