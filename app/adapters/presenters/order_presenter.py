from typing import Any

from app.domain.entities.order import Order


class OrderPresenter:
    @classmethod
    def present(cls, order: Order) -> dict[str, Any]:
        return {
            'id': order.id,
            'products': order.products,
            'customer_id': order.customer_id,
            'status': order.status,
            'total_price': order.total_price,
            'created_at': order.created_at,
            'updated_at': order.updated_at
        }
