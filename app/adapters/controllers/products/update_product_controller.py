from app.adapters.presenters.product_presenter import ProductPresenter
from app.application.use_cases.products.update_product import UpdateProductUseCase
from app.domain.entities.product import Product


class UpdateProductController:
    def __init__(self, use_case: UpdateProductUseCase, presenter: ProductPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, product_id, product_data):
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            category=product_data.category,
            image_path=product_data.image_path,
        )
        updated_product = self.use_case.execute(product_id, product)
        return self.presenter.present(updated_product)
