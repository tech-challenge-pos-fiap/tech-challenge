from sqlalchemy.orm import Session

from app.adapters.gateways.repositories.mappers.customer_mapper import CustomerMapper
from app.adapters.gateways.repositories.mappers.order_mapper import OrderItemMapper, OrderMapper
from app.adapters.gateways.repositories.mappers.product_mapper import ProductMapper
from app.adapters.gateways.repositories.order_repository_port import OrderRepositoryPort
from app.infrastructure.persistence.models.order import OrderItemModel, OrderModel


class OrderRepository(OrderRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def _mapper_to_model(self, order: OrderMapper) -> OrderModel:
        return OrderModel(
            customer_id=order.customer.id if order.customer else None,
            status=order.status,
            total_price=order.total_price,
            items=[
                OrderItemModel(
                    product_id=item.product.id,
                    quantity=item.quantity
                ) for item in order.items
            ]
        )


    def _model_to_mapper(self, instance: OrderModel) -> OrderMapper:
        return OrderMapper(
            id=instance.id,
            items=[OrderItemMapper(
                product=ProductMapper(
                    id=item.product.id,
                    name=item.product.name,
                    description=item.product.description,
                    price=item.product.price,
                    category=item.product.category,
                    image_path=item.product.image_path
                ),
                quantity=item.quantity
            ) for item in instance.items],
            status=instance.status,
            total_price=instance.total_price,
            customer=CustomerMapper(
                id=instance.customer.id,
                name=instance.customer.name,
                email=instance.customer.email,
                cpf=instance.customer.cpf,
            ) if instance.customer else None,
        )

    def save(self, order: OrderMapper) -> OrderMapper:
        order_model = self._mapper_to_model(order)
        self.session.add(order_model)
        self.session.commit()
        self.session.refresh(order_model)
        return self._model_to_mapper(order_model)

    def get(self, order_id: str) -> OrderMapper:
        order_model = self.session.query(OrderModel).filter(OrderModel.id == order_id).first()
        return self._model_to_mapper(order_model) if order_model else None

    def update(self, order_id: str, order_data: OrderMapper) -> OrderMapper:
        order_model = self.session.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order_model:
            return None

        for key, value in order_data.__dict__.items():
            if value is not None:
                setattr(order_model, key, value)

        self.session.commit()
        self.session.refresh(order_model)
        return self._model_to_mapper(order_model)

    def get_all(self, skip: int = 0, limit: int = 10) -> list[OrderMapper]:
        order_models = self.session.query(OrderModel).offset(skip).limit(limit).all()
        return [self._model_to_mapper(order_model) for order_model in order_models]

    def delete(self, order_id: str) -> bool:
        order_model = self.session.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order_model:
            return False

        self.session.delete(order_model)
        self.session.commit()
        return True

    def update_status(self, order_id: str, status: str) -> OrderMapper:
        order_model = self.session.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order_model:
            return None

        order_model.status = status
        self.session.commit()
        self.session.refresh(order_model)
        return self._model_to_mapper(order_model)

    def checkout(self, order_id: str) -> OrderMapper:
        order_model = self.session.query(OrderModel).filter(OrderModel.id == order_id).first()
        if not order_model:
            return None

        # Here you would implement the logic for checking out the order
        # For example, updating the status to 'checked_out'
        order_model.status = 'checked_out'
        self.session.commit()
        self.session.refresh(order_model)
        return self._model_to_mapper(order_model)

    def get_by_customer_id(self, customer_id: str, skip: int = 0, limit: int = 10) -> list[OrderMapper]:
        order_models = (
        self.session.query(OrderModel)
        .filter(OrderModel.customer_id == customer_id)
        .offset(skip)
        .limit(limit)
        .all())
        return [self._model_to_mapper(order_model) for order_model in order_models]

    def get_by_status(self, status: str, skip: int = 0, limit: int = 10) -> list[OrderMapper]:
        order_models = (
        self.session.query(OrderModel)
        .filter(OrderModel.status == status)
        .offset(skip)
        .limit(limit)
        .all())
        return [self._model_to_mapper(order_model) for order_model in order_models]

    def count_orders(self) -> int:
        return self.session.query(OrderModel).count()

    def exists(self, order_id: str) -> bool:
        return self.session.query(OrderModel.id).filter(OrderModel.id == order_id).scalar() is not None
