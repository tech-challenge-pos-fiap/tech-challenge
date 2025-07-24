from app.application.ports.orders.order_repository_gateway import OrderRepositoryGatewayPort
from app.application.ports.payments.payment_repository_gateway import PaymentRepositoryGatewayPort
from app.application.ports.payments.payment_service_gateway import PaymentServiceGatewayPort
from app.domain.entities.order import OrderStatus
from app.domain.entities.payment import Payment


class ProcessPaymentUseCase:
    def __init__(
        self,
        payment_service: PaymentServiceGatewayPort,
        payment_repository: PaymentRepositoryGatewayPort,
        order_repository: OrderRepositoryGatewayPort,
    ):
        self.payment_service = payment_service
        self.payment_repository = payment_repository
        self.order_repository = order_repository

    def execute(self, payment_data: dict) -> Payment:
        self._validate_order(payment_data)
        payment = Payment.create(
            transaction_amount=payment_data["transaction_amount"],
            description=payment_data.get("description"),
            order_id=payment_data["order_id"],
        )
        processed = self.payment_service.process_payment(payment)
        if not processed:
            raise ValueError("Payment processing failed")
        return self.payment_repository.save(payment)

    def _validate_order(self, payment_data: dict) -> None:
        order_id = payment_data["order_id"]
        order = self.order_repository.get(order_id)

        if not order:
            raise ValueError(f"Order {order_id} not found")

        if order.status != OrderStatus.PENDING:
            raise ValueError(
                f"""
                Order {order_id} is not in a valid state for payment processing.
                Current status: {order.status}
                """
            )

        if order.total_price != payment_data["transaction_amount"]:
            raise ValueError(
                f"""
                Payment amount {payment_data['transaction_amount']}
                does not match order total price {order.total_price}.
                """
            )
