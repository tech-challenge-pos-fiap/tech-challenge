from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    description: str
    price: float
    category: str
    image_path: str
