from typing import Any, Dict

from app.application.ports.payments.payment_repository_gateway import PaymentRepositoryGatewayPort
from app.domain.entities.payment import PaymentStatus


class UpdatePaymentStatusUseCase:
    def __init__(self, payment_repository: PaymentRepositoryGatewayPort):
        self.payment_repository = payment_repository

    def execute(self, webhook_data: Dict[str, Any]) -> bool:
        """
        Update payment status based on webhook data from Mercado Pago.

        Args:
            webhook_data: Dictionary containing webhook payload from Mercado Pago

        Returns:
            bool: True if payment was updated successfully, False otherwise
        """
        try:
            # Extract payment ID from webhook data (this is the Mercado Pago ID)
            mp_payment_id = webhook_data.get("id")
            if not mp_payment_id:
                return False

            # Get payment by Mercado Pago ID
            payment = self.payment_repository.get_payment_by_mp_id(str(mp_payment_id))
            if not payment:
                return False

            # Update status based on Mercado Pago status
            mp_status = webhook_data.get("status")
            if mp_status == "approved":
                payment.status = PaymentStatus.APPROVED
            elif mp_status == "rejected":
                payment.status = PaymentStatus.REJECTED
            elif mp_status == "cancelled":
                payment.status = PaymentStatus.CANCELLED
            elif mp_status == "in_process":
                payment.status = PaymentStatus.IN_PROCESS
            elif mp_status == "refunded":
                payment.status = PaymentStatus.REFUNDED
            else:
                payment.status = PaymentStatus.ERROR

            # Update Mercado Pago related fields
            payment.mp_status = mp_status
            payment.mp_status_detail = webhook_data.get("status_detail")
            payment.mp_response = webhook_data

            # Save the updated payment
            self.payment_repository.save(payment)

            return True

        except Exception as e:
            return False
