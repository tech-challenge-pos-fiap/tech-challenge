from dataclasses import dataclass

from app.domain.entities.product import Product


@dataclass
class ProductMapper:
    id: int
    name: str
    description: str
    price: float
    category: str
    image_path: str

    @classmethod
    def from_entity(cls, product: Product) -> 'ProductMapper':
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            image_path=product.image_path
        )

    def to_entity(self) -> Product:
        return Product(
            id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            category=self.category,
            image_path=self.image_path
        )
