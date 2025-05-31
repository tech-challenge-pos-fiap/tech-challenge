from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from requests.exceptions import HTTPError
from requests.models import Response


def test_create_pix_payment_success(client: TestClient):
    payload = {
        "transaction_amount": 100.00,
        "description": "Teste de pagamento PIX",
        "payment_method_id": "pix",
        "payer": {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }

    mock_mp_response = {
        "id": 123456789,
        "status": "pending",
        "transaction_amount": 100.00,
        "point_of_interaction": {
            "transaction_data": {
                "qr_code": "test_qr_code",
                "qr_code_base64": "test_qr_code_base64"
            }
        }
    }

    with patch('app.adapters.external.mercado_pago.pix.MercadoPagoPixClient.create_pix_payment') as mock_create:
        mock_create.return_value = mock_mp_response

        response = client.post('/api/v1/payments/pix', json=payload)
        data = response.json()
        print(data)
        assert response.status_code == 200
        assert data['status'] == 'pending'
        assert data['transaction_amount'] == 100.00
        assert data['qr_code'] == 'test_qr_code'
        assert data['qr_code_base64'] == 'test_qr_code_base64'
        assert data['payer']['email'] == 'test@example.com'

def test_create_pix_payment_invalid_amount(client: TestClient):
    payload = {
        "transaction_amount": -100.00,
        "description": "Teste de pagamento PIX",
        "payment_method_id": "pix",
        "payer": {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }

    response = client.post('/api/v1/payments/pix', json=payload)
    assert response.status_code == 422

def test_create_pix_payment_mp_api_error(client: TestClient):
    payload = {
        "transaction_amount": 100.00,
        "description": "Teste de pagamento PIX",
        "payment_method_id": "pix",
        "payer": {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }

    mock_response = MagicMock(spec=Response)
    mock_response.status_code = 403
    mock_response.json.return_value = {"message": "Forbidden"}
    http_error = HTTPError(response=mock_response)

    with patch('app.adapters.external.mercado_pago.pix.MercadoPagoPixClient.create_pix_payment') as mock_create:
        mock_create.side_effect = http_error
        response = client.post('/api/v1/payments/pix', json=payload)
        assert response.status_code == 403

def test_create_pix_payment_missing_required_fields(client: TestClient):
    payload = {
        "payment_method_id": "pix"
    }
    response = client.post('/api/v1/payments/pix', json=payload)
    assert response.status_code == 422

def test_get_payment_by_id_not_found(client: TestClient):
    response = client.get('/api/v1/payments/999999')
    assert response.status_code == 404

def test_create_pix_payment_with_invalid_order_id(client: TestClient):
    payment_payload = {
        "transaction_amount": 100.00,
        "description": "Test payment with invalid order",
        "payment_method_id": "pix",
        "order_id": 999,
        "payer": {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }

    with patch('app.adapters.persistence.repositories.order_repository.OrderRepository.get') as mock_get_order:
        mock_get_order.return_value = None
        response = client.post('/api/v1/payments/pix', json=payment_payload)
        assert response.status_code == 404
        data = response.json()
        assert "Ordem com ID 999 não encontrada" in data['detail']
