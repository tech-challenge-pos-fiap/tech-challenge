# tests/domain/test_order.py
from decimal import Decimal

import pytest

from app.domain.entities.customer import Customer
from app.domain.entities.order import Order, OrderItem, OrderStatus
from app.domain.entities.product import Product


@pytest.fixture
def product():
    return Product(
        id=1,
        name="Burger",
        price=Decimal("30.00"),
        description="Beef burger",
        category="burguers",
        image_path="burger.jpg",
    )


@pytest.fixture
def customer():
    return Customer(id=1, name="Alice", email="alice@example.com")


def test_order_creation_with_valid_items(product, customer):
    item = OrderItem(product=product, quantity=2)
    order = Order.create(items=[item], customer=customer)

    assert order.total_price == Decimal("60.00")
    assert order.status == OrderStatus.PENDING
    assert order.customer == customer
    assert len(order.items) == 1


def test_order_creation_fails_with_empty_items():
    with pytest.raises(ValueError, match="Order must have at least one item."):
        Order.create(items=[])


def test_order_total_price_with_multiple_items():
    p1 = Product(
        id=1,
        name="Burger",
        price=Decimal("30.00"),
        description="Beef burger",
        category="burguers",
        image_path="burger.jpg",
    )
    p2 = Product(
        id=2,
        name="Fries",
        price=Decimal("10.00"),
        description="French fries",
        category="appetizers",
        image_path="fries.jpg",
    )
    items = [
        OrderItem(product=p1, quantity=1),
        OrderItem(product=p2, quantity=3),
    ]
    order = Order.create(items=items)
    assert order.total_price == Decimal("60.00")
