import json, os, threading
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")
LOCK = threading.Lock()
PAY_FILE = "data/payments.json"


class PaymentLedger:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(PAY_FILE):
            with open(PAY_FILE, "w") as f:
                json.dump({"schema_version": "1.0", "payments": {}}, f, indent=2)

    def _load(self):
        with LOCK:
            with open(PAY_FILE, "r") as f:
                return json.load(f)

    def _save(self, data):
        with LOCK:
            tmp = PAY_FILE + ".tmp"
            with open(tmp, "w") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, PAY_FILE)

    def exists(self, order_id):
        return order_id in self._load()["payments"]

    def record_success(self, order_id, username, amount, payment_id):
        data = self._load()
        if order_id in data["payments"]:
            return False  # idempotency guard

        data["payments"][order_id] = {
            "username": username,
            "amount": amount,
            "status": "SUCCESS",
            "payment_id": payment_id,
            "created_at": datetime.now(IST).isoformat(),
        }
        self._save(data)
        return True
