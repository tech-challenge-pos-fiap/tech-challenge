from decimal import Decimal

import pytest

from app.infrastructure.external.external_payment_service import ExternalPaymentProcessService


class TestExternalPaymentService:
    def test_valid_payment(self):
        """Test that valid payment data passes validation."""
        service = ExternalPaymentProcessService()
        payment_data = {"transaction_amount": Decimal("100.00"), "order_id": 1, "description": "Valid payment"}

        result = service.process_payment(payment_data)
        assert result is True

    def test_invalid_amount_zero(self):
        """Test that zero amount is rejected."""
        service = ExternalPaymentProcessService()
        payment_data = {"transaction_amount": Decimal("0.00"), "order_id": 1}

        result = service.process_payment(payment_data)
        assert result is False

    def test_invalid_amount_negative(self):
        """Test that negative amount is rejected."""
        service = ExternalPaymentProcessService()
        payment_data = {"transaction_amount": Decimal("-10.00"), "order_id": 1}

        result = service.process_payment(payment_data)
        assert result is False

    def test_amount_below_minimum(self):
        """Test that amount below minimum is rejected."""
        service = ExternalPaymentProcessService()
        payment_data = {"transaction_amount": Decimal("0.005"), "order_id": 1}

        result = service.process_payment(payment_data)
        assert result is False

    def test_amount_above_maximum(self):
        """Test that amount above maximum is rejected."""
        service = ExternalPaymentProcessService()
        payment_data = {"transaction_amount": Decimal("1000000.00"), "order_id": 1}

        result = service.process_payment(payment_data)
        assert result is False

    def test_missing_required_fields(self):
        """Test that missing required fields are rejected."""
        service = ExternalPaymentProcessService()

        # Missing transaction_amount
        payment_data_1 = {"order_id": 1}
        result = service.process_payment(payment_data_1)
        assert result is False

        # Missing order_id
        payment_data_2 = {"transaction_amount": Decimal("100.00")}
        result = service.process_payment(payment_data_2)
        assert result is False

    def test_different_amount_formats(self):
        """Test that different amount formats are handled correctly."""
        service = ExternalPaymentProcessService()

        # Decimal format
        payment_data_1 = {"transaction_amount": Decimal("100.00"), "order_id": 1}
        result = service.process_payment(payment_data_1)
        assert result is True

        # Float format
        payment_data_2 = {"transaction_amount": 100.00, "order_id": 1}
        result = service.process_payment(payment_data_2)
        assert result is True

        # String format
        payment_data_3 = {"transaction_amount": "100.00", "order_id": 1}
        result = service.process_payment(payment_data_3)
        assert result is True

    def test_suspicious_amounts(self):
        """Test that suspicious amounts are flagged but allowed."""
        service = ExternalPaymentProcessService()

        # Test suspicious amount (should be flagged but allowed)
        payment_data = {"transaction_amount": Decimal("999.99"), "order_id": 1}

        result = service.process_payment(payment_data)
        assert result is True  # Should still pass validation

    def test_suspicious_description(self):
        """Test that suspicious descriptions are flagged but allowed."""
        service = ExternalPaymentProcessService()

        payment_data = {"transaction_amount": Decimal("100.00"), "order_id": 1, "description": "This is a test payment"}

        result = service.process_payment(payment_data)
        assert result is True  # Should still pass validation

    def test_custom_amount_limits(self):
        """Test custom amount limits."""
        service = ExternalPaymentProcessService()

        # Set custom limits
        service.set_amount_limits(Decimal("10.00"), Decimal("1000.00"))

        # Test amount below new minimum
        payment_data_1 = {"transaction_amount": Decimal("5.00"), "order_id": 1}
        result = service.process_payment(payment_data_1)
        assert result is False

        # Test amount above new maximum
        payment_data_2 = {"transaction_amount": Decimal("1500.00"), "order_id": 1}
        result = service.process_payment(payment_data_2)
        assert result is False

        # Test valid amount within new limits
        payment_data_3 = {"transaction_amount": Decimal("500.00"), "order_id": 1}
        result = service.process_payment(payment_data_3)
        assert result is True

    def test_add_suspicious_amount(self):
        """Test adding custom suspicious amounts."""
        service = ExternalPaymentProcessService()

        # Add custom suspicious amount
        service.add_suspicious_amount(Decimal("123.45"))

        # Test that the new suspicious amount is in the list
        assert Decimal("123.45") in service.suspicious_amounts

    def test_invalid_amount_format(self):
        """Test that invalid amount format raises exception."""
        service = ExternalPaymentProcessService()

        payment_data = {"transaction_amount": "invalid_amount", "order_id": 1}

        result = service.process_payment(payment_data)
        assert result is False  # Should handle exception gracefully

    def test_edge_cases(self):
        """Test edge cases for amount validation."""
        service = ExternalPaymentProcessService()

        # Test minimum valid amount
        payment_data_1 = {"transaction_amount": Decimal("0.01"), "order_id": 1}
        result = service.process_payment(payment_data_1)
        assert result is True

        # Test maximum valid amount
        payment_data_2 = {"transaction_amount": Decimal("999999.99"), "order_id": 1}
        result = service.process_payment(payment_data_2)
        assert result is True
