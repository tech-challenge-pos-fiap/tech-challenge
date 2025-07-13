from sqlalchemy.orm import Session

from app.adapters.gateways.mappers.order_mapper import OrderMapper
from app.adapters.gateways.repositories.order_repository_port import OrderRepositoryPort
from app.infrastructure.persistence.models.order import OrderModel


class OrderRepository(OrderRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def _mapper_to_model(self, order: OrderMapper) -> OrderModel:
        return OrderModel(
            id=order.id,
            products=order.products,
            status=order.status,
            total_price=order.total_price,
            customer_id=order.customer_id,
        )

    def _model_to_mapper(self, instance: OrderModel) -> OrderMapper:
        return OrderMapper(
            id=instance.id,
            products=instance.products,
            status=instance.status,
            total_price=instance.total_price,
            customer_id=instance.customer_id,
            created_at=instance.created_at,
            updated_at=instance.updated_at
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
