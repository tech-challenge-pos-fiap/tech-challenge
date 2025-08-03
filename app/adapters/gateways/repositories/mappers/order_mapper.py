from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from app.adapters.gateways.repositories.mappers.customer_mapper import CustomerMapper
from app.adapters.gateways.repositories.mappers.product_mapper import ProductMapper
from app.domain.entities.order import Order, OrderItem, OrderStatus


@dataclass
class OrderItemMapper:
    product: ProductMapper
    quantity: int

    @classmethod
    def from_entity(cls, order_item: OrderItem) -> "OrderItemMapper":
        return cls(
            product=ProductMapper.from_entity(order_item.product),
            quantity=order_item.quantity,
        )

    def to_entity(self) -> OrderItem:
        return OrderItem(
            product=self.product.to_entity(),
            quantity=self.quantity,
        )


@dataclass
class OrderMapper:
    items: list[OrderItemMapper]
    status: OrderStatus
    total_price: Decimal
    customer: Optional[CustomerMapper] = None
    id: Optional[int] = None

    @classmethod
    def from_entity(cls, order: Order) -> "OrderMapper":
        return cls(
            id=order.id,
            items=[OrderItemMapper.from_entity(item) for item in order.items],
            customer=CustomerMapper.from_entity(order.customer) if order.customer else None,
            status=order.status,
            total_price=order.total_price,
        )

    def to_entity(self) -> Order:
        return Order(
            id=self.id,
            items=[item.to_entity() for item in self.items],
            customer=self.customer.to_entity() if self.customer else None,
            status=self.status,
            total_price=self.total_price,
        )
