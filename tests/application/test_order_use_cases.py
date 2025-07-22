# pylint: disable=redefined-outer-name
from decimal import Decimal

import pytest

from app.application.use_cases.orders.create_order import CreateOrderUseCase
from app.domain.entities.customer import Customer
from app.domain.entities.product import Product


@pytest.fixture
def mock_product_repo(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_customer_repo(mocker):
    return mocker.Mock()


@pytest.fixture
def mock_order_repo(mocker):
    return mocker.Mock()


@pytest.fixture
def use_case(mock_order_repo, mock_product_repo, mock_customer_repo):
    return CreateOrderUseCase(
        order_repository=mock_order_repo,
        product_repository=mock_product_repo,
        customer_repository=mock_customer_repo,
    )


def test_create_order_with_customer(use_case, mock_product_repo, mock_customer_repo, mock_order_repo):
    burger = Product(
        id=1,
        name="Cheeseburger",
        description="Juicy beef burger with cheese",
        price=Decimal("5.99"),
        category="Burgers",
        image_path="/images/burger.jpg"
    )
    customer = Customer(id=1, name="Bob", email="bob@fastfood.com")

    mock_product_repo.filter.return_value = [burger]
    mock_customer_repo.get.return_value = customer
    mock_order_repo.save.side_effect = lambda order: order

    order_data = {
        "items": [{"product_id": 1, "quantity": 2}],
        "customer_id": 1
    }

    order = use_case.execute(order_data)

    assert order.total_price == Decimal("11.98")
    assert order.customer == customer
    mock_product_repo.filter.assert_called_once_with(id=[1])
    mock_customer_repo.get.assert_called_once_with(1)
    mock_order_repo.save.assert_called_once()


def test_create_order_without_customer(use_case, mock_product_repo, mock_order_repo):
    fries = Product(
        id=2,
        name="Fries",
        description="Crispy golden fries",
        price=2.50,
        category="Sides",
        image_path="/images/fries.jpg"
    )

    mock_product_repo.filter.return_value = [fries]
    mock_order_repo.save.side_effect = lambda order: order

    order_data = {
        "items": [{"product_id": 2, "quantity": 3}]
    }

    order = use_case.execute(order_data)

    assert order.total_price == Decimal("7.50")
    assert order.customer is None
    mock_product_repo.filter.assert_called_once_with(id=[2])
    mock_order_repo.save.assert_called_once()


def test_raises_if_product_id_is_invalid(use_case, mock_product_repo):
    mock_product_repo.filter.return_value = []  # product not found

    order_data = {
        "items": [{"product_id": 999, "quantity": 1}]
    }

    with pytest.raises(KeyError):  # current behavior — could change to ValueError in use case
        use_case.execute(order_data)
