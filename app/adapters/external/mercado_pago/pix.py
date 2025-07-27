import os

import requests


class MercadoPagoPixClient:
    def __init__(self):
        self.MP_PAYMENT_URL = os.environ.get("MP_PAYMENT_URL", "https://api.mercadopago.com/v1/payments")
        self.MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN")
        self.MP_IDEMPOTENCY_KEY = os.environ.get("MP_IDEMPOTENCY_KEY")

    def create_pix_payment(self, payment_data: dict) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.MP_ACCESS_TOKEN}",
            "X-Idempotency-Key": self.MP_IDEMPOTENCY_KEY,
        }
        response = requests.post(self.MP_PAYMENT_URL, json=payment_data, headers=headers)
        response.raise_for_status()
        return response.json()
