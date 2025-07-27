from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from app.application.services.payments.create_payment_service import CreatePixPaymentService
from app.application.services.payments.list_payment_service import ListPaymentService


class MockPaymentPort:
    def create_pix_payment(self, payment_data):
        return {
            "id": 1,
            "status": "pending",
            "transaction_amount": payment_data["transaction_amount"],
            "payment_method_id": "pix",
            "qr_code": "test_qr_code",
            "qr_code_base64": "test_qr_code_base64",
            "payer": payment_data.get("payer", {})
        }

    def get_payment_by_id(self, payment_data):
        payment_id = payment_data["id"]
        return {
            "id": payment_id,
            "status": "approved",
            "amount": 100.00,
            "method": "pix"
        }


class MockOrderRepository:
    def get(self, order_id):
        return {"id": order_id, "status": "pending"}

def test_create_pix_payment_service():
    mock_port = MockPaymentPort()
    mock_order_repo = MockOrderRepository()
    service = CreatePixPaymentService(mock_port, mock_order_repo)
    payment_data = {
        "transaction_amount": 100.00,
        "description": "Test payment",
        "payment_method_id": "pix",
        "payer": {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }
    result = service.execute(payment_data)
    assert result["id"] == 1
    assert result["status"] == "pending"
    assert result["transaction_amount"] == 100.00
    assert result["payment_method_id"] == "pix"
    assert result["qr_code"] == "test_qr_code"
    assert result["payer"]["email"] == "test@example.com"

def test_list_payment_service():
    mock_port = MockPaymentPort()
    service = ListPaymentService(mock_port)
    payment_id = 1
    result = service.get_payment_by_id({"id": payment_id})
    assert result["id"] == payment_id
    assert result["status"] == "approved"
    assert result["amount"] == 100.00
    assert result["method"] == "pix"

def test_create_pix_payment_service_with_invalid_data():
    mock_port = MockPaymentPort()
    mock_order_repo = MockOrderRepository()
    service = CreatePixPaymentService(mock_port, mock_order_repo)
    payment_data = {
        "payment_method_id": "pix"
    }
    with pytest.raises(Exception) as exc_info:
        service.execute(payment_data)

def test_create_pix_payment_service_with_mp_error():
    mock_port = MagicMock()
    mock_port.create_pix_payment.side_effect = Exception("MP API Error")
    mock_order_repo = MockOrderRepository()
    service = CreatePixPaymentService(mock_port, mock_order_repo)
    payment_data = {
        "transaction_amount": 100.00,
        "description": "Test payment",
        "payment_method_id": "pix",
        "payer": {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }
    with pytest.raises(Exception) as exc_info:
        service.execute(payment_data)
    assert str(exc_info.value) == "MP API Error"
