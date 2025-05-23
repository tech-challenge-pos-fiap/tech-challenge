from sqlalchemy import Column, Integer, String

from app.adapters.persistence.models.base import TimestampMixin


class CustomerModel(TimestampMixin):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, nullable=True)
    cpf = Column(String(11), unique=True, nullable=True)
