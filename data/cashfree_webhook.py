import hmac, hashlib, json
from payment_ledger import PaymentLedger
from subscription_manager import SubscriptionManager

CASHFREE_SECRET = os.getenv("CASHFREE_WEBHOOK_SECRET")


def verify_signature(payload, signature):
    digest = hmac.new(
        CASHFREE_SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(digest, signature)


def handle_webhook(headers, body):
    signature = headers.get("x-webhook-signature")
    if not verify_signature(body, signature):
        return {"status": "invalid signature"}, 401

    data = json.loads(body)
    order_id = data["order_id"]
    payment_status = data["order_status"]

    if payment_status != "PAID":
        return {"status": "ignored"}, 200

    username = data["customer_details"]["customer_id"]
    amount = data["order_amount"]
    payment_id = data["payment_id"]

    ledger = PaymentLedger()
    created = ledger.record_success(
        order_id, username, amount, payment_id
    )

    if created:
        SubscriptionManager().grant_subscription(username, days=30)

    return {"status": "ok"}, 200
