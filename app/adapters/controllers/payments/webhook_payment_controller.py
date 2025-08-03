from typing import Any, Dict

from app.application.use_cases.payments.update_payment_status import UpdatePaymentStatusUseCase


class WebhookPaymentController:
    def __init__(self, use_case: UpdatePaymentStatusUseCase):
        self.use_case = use_case

    def execute(self, webhook_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Process webhook from Mercado Pago and update payment status.

        Args:
            webhook_data: Dictionary containing webhook payload from Mercado Pago

        Returns:
            Dict with success/error message
        """
        success = self.use_case.execute(webhook_data)

        if success:
            return {"message": "Payment status updated successfully"}
        else:
            return {"message": "Failed to update payment status"}
