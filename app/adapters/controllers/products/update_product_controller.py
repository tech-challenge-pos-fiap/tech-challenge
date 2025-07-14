from app.adapters.presenters.product_presenter import ProductPresenter
from app.application.use_cases.products.update_product import UpdateProductUseCase


class UpdateProductController:
    def __init__(self, use_case: UpdateProductUseCase, presenter: ProductPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, product_id, product_data):
        product = self.use_case.execute(product_id, product_data)
        return self.presenter.present(product)
