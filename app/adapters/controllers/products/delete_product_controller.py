from app.application.use_cases.products.delete_product import DeleteProductUseCase


class DeleteProductController:
    def __init__(self, use_case: DeleteProductUseCase):
        self.use_case = use_case

    def execute(self, product_id) -> bool:
        return self.use_case.execute(product_id)
