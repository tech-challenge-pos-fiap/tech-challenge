from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:
    name: str
    description: str
    price: float
    category: str
    image_path: str
    id: Optional[int] = field(default=None)
