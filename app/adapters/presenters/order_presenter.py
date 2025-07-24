from dataclasses import asdict
from typing import Any

from app.domain.entities.order import Order


class OrderPresenter:
    @classmethod
    def present(cls, order: Order) -> dict[str, Any]:
        return asdict(order)
