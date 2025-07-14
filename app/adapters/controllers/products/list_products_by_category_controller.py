from app.adapters.presenters.product_presenter import ProductPresenter
from app.application.use_cases.products.list_products_by_category import ListProductsByCategoryUseCase


class ListProductsByCategoryController:
    def __init__(self, use_case: ListProductsByCategoryUseCase, presenter: ProductPresenter):
        self.use_case = use_case
        self.presenter = presenter

    def execute(self, category: str, skip: int = 0, limit: int = 10):
        products = self.use_case.execute(category, skip, limit)
        return self.presenter.present_list(products)
