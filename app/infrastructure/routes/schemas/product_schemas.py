from pydantic import BaseModel

from app.infrastructure.persistence.models.product import ProductCategory


class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: float
    category: ProductCategory
    image_path: str


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: ProductCategory
    image_path: str
