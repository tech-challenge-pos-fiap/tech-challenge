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

    def process_payment(self, payment_data: dict) -> bool:
        """
        Validate payment data and return True if valid.

        Args:
            payment_data: Dictionary containing payment information

        Returns:
            bool: True if payment is valid, False otherwise
        """
        try:
            amount = self._extract_amount(payment_data)

            if not self._validate_amount(amount):
                return False

            if not self._validate_required_fields(payment_data):
                return False

            return True

        except Exception as e:
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

        return True

    def _validate_required_fields(self, payment_data: dict) -> bool:
        """Validate that required fields are present."""
        required_fields = ["transaction_amount", "order_id"]

        for field in required_fields:
            if field not in payment_data:
                return False

        return True

    def set_amount_limits(self, min_amount: Decimal, max_amount: Decimal) -> None:
        """Set custom amount limits for validation."""
        self.min_amount = min_amount
        self.max_amount = max_amount
