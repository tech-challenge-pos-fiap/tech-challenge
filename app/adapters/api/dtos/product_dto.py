from pydantic import BaseModel

from app.adapters.persistence.models.product import ProductCategory


class Product(BaseModel):
    name: str
    description: str
    price: float
    category: ProductCategory

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: ProductCategory
