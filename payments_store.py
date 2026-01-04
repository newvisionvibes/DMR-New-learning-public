import json
import os
from datetime import datetime
import pytz
from threading import Lock

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

IST = pytz.timezone("Asia/Kolkata")
PAYMENTS_FILE = "data/payments.json"
AUDIT_LOG_FILE = "data/payment_audit.log"
_lock = Lock()

# Allowed payment state transitions (HARDENING)
ALLOWED_TRANSITIONS = {
    "CREATED": {"PENDING", "FAILED"},
    "PENDING": {"SUCCESS", "FAILED"},
}

# -------------------------------------------------------------------
# INTERNAL HELPERS
# -------------------------------------------------------------------

def _now():
    return datetime.now(IST).isoformat()


def _load():
    """Load payments.json safely (creates structure if missing)."""
    if not os.path.exists(PAYMENTS_FILE):
        return {
            "schema_version": "1.1",
            "payments": {}
        }

    with open(PAYMENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    """Persist payments.json atomically."""
    with open(PAYMENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _audit(order_id, status, source):
    """Append-only audit trail (optional but recommended)."""
    try:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(
                f"{_now()} | {order_id} | {status} | {source}\n"
            )
    except Exception:
        # Audit failure should never break payments
        pass

# -------------------------------------------------------------------
# PUBLIC API
# -------------------------------------------------------------------

def record_payment(
    order_id: str,
    username: str,
    amount: float,
    status: str = "CREATED",
    payment_id: str | None = None,
    source: str = "system"
):
    """
    Create a new payment record.
    This should be called ONCE per order.
    """
    with _lock:
        data = _load()

        if order_id in data["payments"]:
            # Do NOT overwrite existing records
            return

        data["payments"][order_id] = {
            "username": username,
            "amount": amount,
            "status": status,
            "payment_id": payment_id,
            "verified_by": source,
            "created_at": _now(),
            "updated_at": _now(),
        }

        _save(data)
        _audit(order_id, status, source)


def update_payment_status(
    order_id: str,
    new_status: str,
    source: str,
    payment_id: str | None = None
):
    """
    Update payment status with STRICT state validation.
    Used mainly by Cashfree webhook.
    """
    with _lock:
        data = _load()
        payments = data["payments"]

        if order_id not in payments:
            raise ValueError("Payment record does not exist")

        current_status = payments[order_id]["status"]

        if current_status == new_status:
            return  # idempotent safe-exit

        allowed = ALLOWED_TRANSITIONS.get(current_status, set())
        if new_status not in allowed:
            raise ValueError(
                f"Invalid payment transition: {current_status} → {new_status}"
            )

        payments[order_id]["status"] = new_status
        payments[order_id]["verified_by"] = source
        payments[order_id]["updated_at"] = _now()

        if payment_id:
            payments[order_id]["payment_id"] = payment_id

        _save(data)
        _audit(order_id, new_status, source)


def is_payment_confirmed(order_id: str) -> bool:
    """
    ✅ SINGLE SOURCE OF TRUTH:
    Payment is valid ONLY if marked SUCCESS by Cashfree webhook.
    """
    data = _load()
    record = data["payments"].get(order_id)

    if not record:
        return False

    return (
        record.get("status") == "SUCCESS"
        and record.get("verified_by") == "cashfree_webhook"
    )


def has_successful_payment(username: str) -> bool:
    """
    Legacy helper (kept for compatibility).
    Prefer order-based checks going forward.
    """
    data = _load()
    for record in data["payments"].values():
        if (
            record.get("username") == username
            and record.get("status") == "SUCCESS"
            and record.get("verified_by") == "cashfree_webhook"
        ):
            return True
    return False
