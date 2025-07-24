from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.models.base import TimestampMixin


class ProductCategory(str, Enum):
    BURGUERS = 'burguers'
    DRINKS = 'drinks'
    APPETIZERS = 'appetizers'
    DESSERTS = 'desserts'


class ProductModel(TimestampMixin):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_path: Mapped[str] = mapped_column(String(255), nullable=True)
    category: Mapped[ProductCategory] = mapped_column(
        SqlEnum(
            ProductCategory, name="productcategory", native_enum=True,
            values_callable=lambda x: [e.value for e in ProductCategory]
        ),
        nullable=False
    )
