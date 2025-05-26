from sqlalchemy.orm import Session

from app.adapters.persistence.models.order import OrderModel, OrderStatus, ProductOrderModel
from app.adapters.persistence.models.product import ProductModel
from app.application.ports.order_repository_port import OrderRepositoryPort
from app.domain.models.order import Order


class OrderRepository(OrderRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            products=[
                {
                    "product": product.__dict__,
                } for product in model.products
            ],
            customer_id=model.customer_id,
            status=model.status,
            total_price=model.total_price,
            created_at=model.created_at.isoformat(),
            updated_at=model.updated_at.isoformat(),
        )

    def create(self, order_data: dict) -> Order:
        """Create a new order."""
        products = order_data.get("products")
        order_data["total_price"] = 0
        if products:
            for product in products:
                product_id = product.get("product_id")
                quantity = product.get("quantity")

                if product_id and quantity:
                    product_model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
                    if product_model:
                        order_data["total_price"] += (product_model.price * int(quantity))
                    else:
                        raise ValueError(f"Product with ID {product_id} not found.")

        order = OrderModel(
            status=OrderStatus('pending'),
            customer_id=order_data.get("customer_id", None),
            total_price=order_data.get("total_price"),
        )
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)

        for product_data in products:
            product_id = product_data.get("product_id")
            quantity = product_data.get("quantity")

            product_model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
            if product_model:
                stmt = ProductOrderModel.insert().values(
                    product_id=product_id,
                    order_id=order.id,
                    quantity=quantity,
                )
                self.db.execute(stmt)

            self.db.commit()

        return self._to_domain(order)

    def get(self, order_id: int) -> Order:
        """Get an order by ID."""
        order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if order:
            return self._to_domain(order)
        return None

    def update(self, order_id: int, order_data: dict) -> Order:
        """Update an existing order."""
        order = self.db.query(OrderModel).filter(OrderModel.id == order_id).first()
        if order:
            for key, value in order_data.items():
                setattr(order, key, value)
            self.db.commit()
            self.db.refresh(order)
            return self._to_domain(order)
        return None

    def get_all(self, skip: int = 0, limit: int = 10) -> list[Order]:
        """List orders with pagination."""
        results = self.db.query(OrderModel).offset(skip).limit(limit).all()
        return [
            self._to_domain(order)
            for order in results
        ]
