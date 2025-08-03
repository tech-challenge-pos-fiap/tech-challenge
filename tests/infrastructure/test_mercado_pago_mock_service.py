import pytest
from decimal import Decimal
from datetime import datetime

from app.domain.entities.payment import Payment, PaymentMethod, PaymentStatus
from app.infrastructure.external.mercado_pago_mock_service import MercadoPagoMockService


class TestMercadoPagoMockService:
    
    def test_create_payment_success(self):
        """Test successful payment creation."""
        service = MercadoPagoMockService(success_rate=1.0)
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        response = service.create_payment(payment)
        
        assert response["status"] == "approved"
        assert response["status_detail"] == "accredited"
        assert response["transaction_amount"] == 100.0
        assert response["payment_method_id"] == "pix"
        assert "id" in response
        assert "date_created" in response
        assert "payer" in response
        assert "metadata" in response
    
    def test_create_payment_failure(self):
        """Test failed payment creation."""
        service = MercadoPagoMockService(success_rate=0.0)
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        response = service.create_payment(payment)
        
        assert response["status"] == "rejected"
        assert response["status_detail"] == "cc_rejected_bad_filled_security_code"
        assert response["transaction_amount"] == 100.0
    
    def test_get_payment_status(self):
        """Test getting payment status."""
        service = MercadoPagoMockService()
        payment = Payment.create(
            transaction_amount=Decimal("50.00"),
            description="Test payment",
            order_id=1
        )
        
        # Create payment first
        create_response = service.create_payment(payment)
        payment_id = create_response["id"]
        
        # Get status
        status_response = service.get_payment_status(payment_id)
        
        assert status_response["id"] == payment_id
        assert status_response["status"] in ["approved", "rejected"]
        assert status_response["transaction_amount"] == 50.0
    
    def test_get_payment_status_not_found(self):
        """Test getting status of non-existent payment."""
        service = MercadoPagoMockService()
        
        with pytest.raises(ValueError, match="Payment non_existent not found"):
            service.get_payment_status("non_existent")
    
    def test_refund_payment(self):
        """Test refunding a payment."""
        service = MercadoPagoMockService()
        payment = Payment.create(
            transaction_amount=Decimal("75.00"),
            description="Test payment",
            order_id=1
        )
        
        # Create payment first
        create_response = service.create_payment(payment)
        payment_id = create_response["id"]
        
        # Refund payment
        refund_response = service.refund_payment(payment_id, 50.0)
        
        assert refund_response["payment_id"] == payment_id
        assert refund_response["amount"] == 50.0
        assert refund_response["status"] == "approved"
        assert "id" in refund_response
        assert "date_created" in refund_response
    
    def test_refund_payment_full_amount(self):
        """Test refunding full payment amount."""
        service = MercadoPagoMockService()
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Create payment first
        create_response = service.create_payment(payment)
        payment_id = create_response["id"]
        
        # Refund full amount
        refund_response = service.refund_payment(payment_id)
        
        assert refund_response["payment_id"] == payment_id
        assert refund_response["amount"] == 100.0
        assert refund_response["status"] == "approved"
    
    def test_refund_payment_not_found(self):
        """Test refunding non-existent payment."""
        service = MercadoPagoMockService()
        
        with pytest.raises(ValueError, match="Payment non_existent not found"):
            service.refund_payment("non_existent")
    
    def test_set_success_rate(self):
        """Test setting success rate."""
        service = MercadoPagoMockService(success_rate=0.5)
        
        # Test with different success rates
        service.set_success_rate(1.0)
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        response = service.create_payment(payment)
        assert response["status"] == "approved"
        
        service.set_success_rate(0.0)
        response = service.create_payment(payment)
        assert response["status"] == "rejected"
    
    def test_clear_payments(self):
        """Test clearing stored payments."""
        service = MercadoPagoMockService()
        payment = Payment.create(
            transaction_amount=Decimal("100.00"),
            description="Test payment",
            order_id=1
        )
        
        # Create payment
        create_response = service.create_payment(payment)
        payment_id = create_response["id"]
        
        # Verify payment exists
        status_response = service.get_payment_status(payment_id)
        assert status_response["id"] == payment_id
        
        # Clear payments
        service.clear_payments()
        
        # Verify payment no longer exists
        with pytest.raises(ValueError):
            service.get_payment_status(payment_id)
    
    def test_payment_storage_persistence(self):
        """Test that payments are stored and can be retrieved."""
        service = MercadoPagoMockService()
        payment = Payment.create(
            transaction_amount=Decimal("25.00"),
            description="Test payment",
            order_id=1
        )
        
        # Create multiple payments
        response1 = service.create_payment(payment)
        response2 = service.create_payment(payment)
        
        # Verify both payments are stored
        status1 = service.get_payment_status(response1["id"])
        status2 = service.get_payment_status(response2["id"])
        
        assert status1["id"] == response1["id"]
        assert status2["id"] == response2["id"]
        assert status1["id"] != status2["id"] 