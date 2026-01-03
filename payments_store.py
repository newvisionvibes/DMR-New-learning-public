import json
import os
from datetime import datetime
import pytz
from threading import Lock

IST = pytz.timezone("Asia/Kolkata")
PAYMENTS_FILE = "data/payments.json"
_lock = Lock()


def _load():
    if not os.path.exists(PAYMENTS_FILE):
        return {"schema_version": "1.0", "payments": {}}

    with open(PAYMENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(PAYMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_payment(order_id, username, amount, status, payment_id=None):
    with _lock:
        data = _load()

        data["payments"][order_id] = {
            "username": username,
            "amount": amount,
            "status": status,
            "payment_id": payment_id,
            "created_at": datetime.now(IST).isoformat(),
        }

        _save(data)


def has_successful_payment(username):
    data = _load()
    for p in data["payments"].values():
        if p["username"] == username and p["status"] == "SUCCESS":
            return True
    return False
