from decimal import Decimal
from typing import Any, Dict

from app.adapters.gateways.services.payment_process_service import PaymentProcessServicePort


class ExternalPaymentProcessService(PaymentProcessServicePort):
    """
    Payment Validation Service

    This service validates payment data before processing.
    It performs basic validations and can be extended for more complex rules.

    Validations:
    - Amount must be positive
    - Amount must be within reasonable limits
    - Payment data must contain required fields
    - Basic fraud detection (simple rules)
    """

    def __init__(self):
        self.min_amount = Decimal("0.01")
        self.max_amount = Decimal("999999.99")
        self.suspicious_amounts = [Decimal("999.99"), Decimal("1000.00"), Decimal("5000.00")]

    def process_payment(self, payment_data: dict) -> bool:
        """
        Validate payment data and return True if valid.

        Args:
            payment_data: Dictionary containing payment information

        Returns:
            bool: True if payment is valid, False otherwise
        """
        try:
            # Extract amount from payment data
            amount = self._extract_amount(payment_data)

            # Perform validations
            if not self._validate_amount(amount):
                return False

            if not self._validate_required_fields(payment_data):
                return False

            if not self._validate_fraud_detection(payment_data):
                return False

            # All validations passed
            return True

        except Exception as e:
            # Log error (in production, you'd want proper logging)
            print(f"Payment validation error: {e}")
            return False

    def _extract_amount(self, payment_data: dict) -> Decimal:
        """Extract amount from payment data."""
        amount = payment_data.get("transaction_amount")

        if isinstance(amount, (int, float)):
            return Decimal(str(amount))
        elif isinstance(amount, str):
            return Decimal(amount)
        elif isinstance(amount, Decimal):
            return amount
        else:
            raise ValueError("Invalid amount format")

    def _validate_amount(self, amount: Decimal) -> bool:
        """Validate payment amount."""
        # Check if amount is positive
        if amount <= 0:
            return False

        # Check if amount is within limits
        if amount < self.min_amount or amount > self.max_amount:
            return False

        # Check for suspicious amounts (simple fraud detection)
        if amount in self.suspicious_amounts:
            # In production, you might want to flag these for review
            # For now, we'll allow them but log
            print(f"Warning: Suspicious amount detected: {amount}")

        return True

    def _validate_required_fields(self, payment_data: dict) -> bool:
        """Validate that required fields are present."""
        required_fields = ["transaction_amount", "order_id"]

        for field in required_fields:
            if field not in payment_data:
                return False

        return True

    def _validate_fraud_detection(self, payment_data: dict) -> bool:
        """Basic fraud detection rules."""
        # Check for rapid successive payments (simple rule)
        # In production, you'd want more sophisticated fraud detection

        # Check if description is suspicious
        description = payment_data.get("description", "").lower()
        suspicious_keywords = ["test", "fake", "invalid", "suspicious"]

        for keyword in suspicious_keywords:
            if keyword in description:
                print(f"Warning: Suspicious description detected: {description}")
                # For now, we'll allow it but log
                # In production, you might want to reject these

        return True

    def set_amount_limits(self, min_amount: Decimal, max_amount: Decimal) -> None:
        """Set custom amount limits for validation."""
        self.min_amount = min_amount
        self.max_amount = max_amount

    def add_suspicious_amount(self, amount: Decimal) -> None:
        """Add an amount to the suspicious amounts list."""
        if amount not in self.suspicious_amounts:
            self.suspicious_amounts.append(amount)
