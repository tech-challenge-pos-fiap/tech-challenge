from app.domain.entities.product import Product


class ProductPresenter:
    @classmethod
    def present(cls, product: Product) -> dict[str, str | float | int | None]:
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "image_path": product.image_path,
        }
