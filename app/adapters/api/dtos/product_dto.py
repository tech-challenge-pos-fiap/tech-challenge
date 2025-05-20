from pydantic import BaseModel


class ProductDTO(BaseModel):
    name: str
    description: str
    price: float
    category: str
