import requests
import os


class MercadoPagoPixClient:

    def __init__(self):
        self.MP_PAYMENT_URL = os.environ.get("MP_PAYMENT_URL", "https://api.mercadopago.com/v1/payments")
        self.MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "TEST-4764637462089045-051118-dee7a50610a692dfc56357c172b61f07-201284269")
        self.MP_IDEMPOTENCY_KEY = os.environ.get("X-Idempotency-Key", "TEST-172ee772-80c7-4643-b5b0-be1656228162")

    def create_pix_payment(self, payment_data: dict) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.MP_ACCESS_TOKEN}",
            "X-Idempotency-Key": self.MP_IDEMPOTENCY_KEY,
        }

        response = requests.post(self.MP_PAYMENT_URL, json=payment_data, headers=headers)
        response.raise_for_status()
        return response.json()
