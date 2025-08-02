from typing import Optional

from app.application.ports.customers.customer_repository_gateway import CustomerRepositoryGatewayPort
from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.application.ports.products.product_repository_gateway import ProductRepositoryGatewayPort
from app.domain.entities.customer import Customer
from app.domain.entities.order import Order, OrderItem


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepositoryGatewayPort,
        product_repository: ProductRepositoryGatewayPort,
        customer_repository: CustomerRepositoryGatewayPort,
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.customer_repository = customer_repository

    def execute(self, order_data: dict) -> Order:
        """Create a new order."""
        product_ids = [item["product_id"] for item in order_data["items"]]
        products = self.product_repository.filter(id=product_ids)
        product_map = {product.id: product for product in products}

        order_items = []
        for item in order_data["items"]:
            product = product_map[item["product_id"]]
            order_items.append(OrderItem(product=product, quantity=item["quantity"]))

        customer: Optional[Customer] = None
        if "customer_id" in order_data:
            customer = self.customer_repository.get(order_data.get("customer_id"))

        order = Order.create(order_items, customer)
        return self.order_repository.save(order)
