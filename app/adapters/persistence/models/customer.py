from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship
from .base import TimestampMixin

class CustomerModel(TimestampMixin):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    cpf = Column(String(11), unique=True, nullable=True)
    orders: Mapped[List["OrderModel"]] = relationship("OrderModel", back_populates="customer")
