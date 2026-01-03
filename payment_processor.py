import json
import os
from datetime import datetime, timedelta
import pytz
import logging

from subscription_manager import SubscriptionManager

IST = pytz.timezone("Asia/Kolkata")
logger = logging.getLogger(__name__)

PAYMENTS_FILE = "data/payments.json"


class PaymentProcessor:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(PAYMENTS_FILE):
            with open(PAYMENTS_FILE, "w") as f:
                json.dump({"schema_version": "1.0", "payments": {}}, f, indent=2)

    def record_payment(self, payload: dict):
        """
        Idempotent payment recorder + subscription activator
        """
        order_id = payload["order_id"]

        data = self._load()

        # 🔁 Idempotency guard
        if order_id in data["payments"]:
            logger.info(f"Payment already processed: {order_id}")
            return

        payment = {
            "username": payload["username"],
            "amount": payload["amount"],
            "status": payload["status"],
            "payment_id": payload["payment_id"],
            "created_at": datetime.now(IST).isoformat()
        }

        data["payments"][order_id] = payment
        self._save(data)

        if payload["status"] == "SUCCESS":
            self._activate_subscription(payload["username"])

    def _activate_subscription(self, username: str):
        manager = SubscriptionManager()
        manager.activate_or_extend(username, days=30)

    def _load(self):
        with open(PAYMENTS_FILE, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(PAYMENTS_FILE, "w") as f:
            json.dump(data, f, indent=2)
