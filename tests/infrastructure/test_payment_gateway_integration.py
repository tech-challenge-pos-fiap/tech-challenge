import pytest
from decimal import Decimal
from unittest.mock import Mock, patch

from app.adapters.gateways.payment_service_gateway import PaymentServiceGateway
from app.domain.entities.payment import Payment, PaymentStatus
from app.infrastructure.external.mercado_pago_mock_service import MercadoPagoMockService
from app.infrastructure.external.external_payment_service import ExternalPaymentProcessService


class TestPaymentGatewayIntegration:
    
    def test_payment_gateway_with_valid_payment(self):
        """Test that payment gateway works correctly with valid payment."""
        # Arrange
        validation_service = ExternalPaymentProcessService()
        mock_service = MercadoPagoMockService(success_rate=1.0)
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Act
        result = gateway.process_payment(payment)
        
        # Assert
        assert result is True
        assert payment.mp_payment_id is not None
        assert payment.mp_status == "approved"
        assert payment.status == PaymentStatus.APPROVED
        assert payment.mp_response is not None
    
    def test_payment_gateway_with_invalid_payment(self):
        """Test that payment gateway rejects invalid payments."""
        # Arrange
        validation_service = ExternalPaymentProcessService()
        mock_service = MercadoPagoMockService(success_rate=1.0)
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("0.00"),  # Invalid amount
            description="Test payment",
            order_id=1
        )
        
        # Act
        result = gateway.process_payment(payment)
        
        # Assert
        assert result is False
        assert payment.status == PaymentStatus.REJECTED
        assert payment.mp_response == {"error": "Payment validation failed"}
    
    def test_payment_gateway_with_failed_mp_payment(self):
        """Test that payment gateway handles failed MP payments correctly."""
        # Arrange
        validation_service = ExternalPaymentProcessService()
        mock_service = MercadoPagoMockService(success_rate=0.0)
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Act
        result = gateway.process_payment(payment)
        
        # Assert
        assert result is True  # Validation passed, but MP failed
        assert payment.mp_payment_id is not None
        assert payment.mp_status == "rejected"
        assert payment.status == PaymentStatus.REJECTED
        assert payment.mp_response is not None
    
    def test_payment_gateway_with_mp_service_exception(self):
        """Test that payment gateway handles MP service exceptions correctly."""
        # Arrange
        validation_service = ExternalPaymentProcessService()
        mock_service = Mock()
        mock_service.create_payment.side_effect = Exception("Service error")
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Act
        result = gateway.process_payment(payment)
        
        # Assert
        assert result is False  # Should return False on exception
        assert payment.status == PaymentStatus.IN_PROCESS
        assert payment.mp_response == {"error": "Service error"}
    
    def test_payment_gateway_with_validation_exception(self):
        """Test that payment gateway handles validation exceptions correctly."""
        # Arrange
        validation_service = Mock()
        validation_service.process_payment.side_effect = Exception("Validation error")
        mock_service = MercadoPagoMockService()
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Act
        result = gateway.process_payment(payment)
        
        # Assert
        assert result is False  # Should return False on validation exception
        assert payment.status == PaymentStatus.REJECTED
        assert payment.mp_response == {"error": "Payment validation failed"}
    
    def test_get_payment_status(self):
        """Test getting payment status through gateway."""
        # Arrange
        validation_service = ExternalPaymentProcessService()
        mock_service = MercadoPagoMockService()
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("50.00"),
            description="Test payment",
            order_id=1
        )
        
        # Create payment first
        create_response = mock_service.create_payment(payment)
        payment_id = create_response["id"]
        
        # Act
        status = gateway.get_payment_status(payment_id)
        
        # Assert
        assert status["id"] == payment_id
        assert "status" in status
        assert "transaction_amount" in status
    
    def test_refund_payment(self):
        """Test refunding payment through gateway."""
        # Arrange
        validation_service = ExternalPaymentProcessService()
        mock_service = MercadoPagoMockService()
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Create payment first
        create_response = mock_service.create_payment(payment)
        payment_id = create_response["id"]
        
        # Act
        refund = gateway.refund_payment(payment_id, 50.0)
        
        # Assert
        assert refund["payment_id"] == payment_id
        assert refund["amount"] == 50.0
        assert refund["status"] == "approved"
    
    def test_payment_gateway_initialization(self):
        """Test that payment gateway can be initialized with both services."""
        # Arrange & Act
        validation_service = ExternalPaymentProcessService()
        mock_service = MercadoPagoMockService()
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        # Assert
        assert gateway.validation_service is validation_service
        assert gateway.mp_service is mock_service
    
    def test_payment_gateway_with_real_service_mock(self):
        """Test payment gateway with a mock of the real service."""
        # Arrange
        validation_service = ExternalPaymentProcessService()
        mock_real_service = Mock()
        mock_real_service.create_payment.return_value = {
            "id": "mp_123456789",
            "status": "approved",
            "status_detail": "accredited",
            "transaction_amount": 100.0
        }
        
        gateway = PaymentServiceGateway(validation_service, mock_real_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Act
        result = gateway.process_payment(payment)
        
        # Assert
        assert result is True
        assert payment.mp_payment_id == "mp_123456789"
        assert payment.mp_status == "approved"
        assert payment.status == PaymentStatus.APPROVED
        mock_real_service.create_payment.assert_called_once_with(payment)
    
    def test_payment_gateway_validation_before_mp(self):
        """Test that validation happens before MP processing."""
        # Arrange
        validation_service = Mock()
        validation_service.process_payment.return_value = False  # Validation fails
        mock_service = MercadoPagoMockService()
        gateway = PaymentServiceGateway(validation_service, mock_service)
        
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Act
        result = gateway.process_payment(payment)
        
        # Assert
        assert result is False
        assert payment.status == PaymentStatus.REJECTED
        # MP service should not be called
        assert payment.mp_payment_id is None
        assert payment.mp_status is None 