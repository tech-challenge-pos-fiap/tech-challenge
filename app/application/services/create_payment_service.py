from app.application.ports.payment_port import PaymentPort


class CreatePixPaymentService:
    def __init__(self, payment_port: PaymentPort):
        self.payment_port = payment_port

    def execute(self, payment_data: dict) -> dict:
        payment_data["payment_method_id"] = "pix"
        mp_response = self.payment_port.create_pix_payment(payment_data)
        
        return {
            "id": str(mp_response["id"]),
            "status": mp_response["status"],
            "qr_code": mp_response["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": mp_response["point_of_interaction"]["transaction_data"]["qr_code_base64"],
            "transaction_amount": mp_response["transaction_amount"]
        }
