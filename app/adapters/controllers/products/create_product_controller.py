from app.adapters.presenters.product_presenter import ProductPresenter
from app.application.use_cases.products.create_product import CreateProductUseCase


class CreateProductController:
    def __init__(self, use_case: CreateProductUseCase, presenter: ProductPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, product_data):
        product = self.use_case.execute(product_data)
        return self.presenter.present(product)
