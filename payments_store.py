import json
import os
from datetime import datetime, timedelta
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


def record_payment(
    order_id: str,
    username: str,
    amount: float,
    status: str,
    payment_id: str,
    plan: str,
    verified_by: str = "cashfree_webhook",
):
    with _lock:
        data = _load()
        now = datetime.now(IST)

        # Plan-based expiry
        if plan == "annual":
            expires_at = now + timedelta(days=365)
        else:
            expires_at = now + timedelta(days=30)

        data["payments"][order_id] = {
            "username": username,
            "amount": amount,
            "status": status,
            "payment_id": payment_id,
            "plan": plan,
            "verified_by": verified_by,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
        }

        _save(data)


def get_latest_active_payment(username: str):
    data = _load()
    now = datetime.now(IST)

    valid = []

    for p in data["payments"].values():
        if p.get("username") != username:
            continue
        if p.get("status") != "SUCCESS":
            continue
        if p.get("verified_by") != "cashfree_webhook":
            continue

        try:
            expires = datetime.fromisoformat(p["expires_at"])
        except Exception:
            continue

        if expires > now:
            valid.append(expires)

    return max(valid) if valid else None


def has_active_subscription(username: str) -> bool:
    return get_latest_active_payment(username) is not None


def days_left(username: str) -> int:
    expiry = get_latest_active_payment(username)
    if not expiry:
        return 0
    return max((expiry - datetime.now(IST)).days, 0)
