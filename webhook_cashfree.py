"""
CASHFREE WEBHOOK HANDLER – PHASE 5.1.4
------------------------------------
This is the ONLY authority allowed to mark payments as SUCCESS.

SECURITY RULES:
- Signature verification mandatory
- POST only
- SUCCESS status only
- Idempotent writes
"""

import json
import hmac
import hashlib
import logging
import os
from datetime import datetime

from fastapi import APIRouter, Request, HTTPException

from payments_store import record_payment

logger = logging.getLogger(__name__)

router = APIRouter()

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

CASHFREE_WEBHOOK_SECRET = os.getenv("CASHFREE_WEBHOOK_SECRET")

if not CASHFREE_WEBHOOK_SECRET:
    logger.warning("⚠️ CASHFREE_WEBHOOK_SECRET not set")


# -------------------------------------------------------------------
# SIGNATURE VERIFICATION
# -------------------------------------------------------------------

def _verify_signature(raw_body: bytes, received_signature: str) -> bool:
    """
    Verify Cashfree webhook signature using HMAC SHA256
    """
    computed = hmac.new(
        CASHFREE_WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(computed, received_signature)


# -------------------------------------------------------------------
# WEBHOOK ENDPOINT
# -------------------------------------------------------------------

@router.post("/webhook/cashfree")
async def cashfree_webhook(request: Request):
    """
    Cashfree payment webhook endpoint
    """

    if not CASHFREE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret missing")

    raw_body = await request.body()
    signature = request.headers.get("x-webhook-signature")

    if not signature:
        logger.warning("Webhook rejected: missing signature")
        raise HTTPException(status_code=401, detail="Signature missing")

    if not _verify_signature(raw_body, signature):
        logger.warning("Webhook rejected: invalid signature")
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        logger.error("Webhook rejected: invalid JSON")
        raise HTTPException(status_code=400, detail="Invalid payload")

    logger.info(f"📥 Cashfree webhook received: {payload}")

    # ----------------------------------------------------------------
    # EXTRACT FIELDS (STRICT)
    # ----------------------------------------------------------------

    order_id = payload.get("order_id")
    payment_status = payload.get("payment_status")
    payment_id = payload.get("payment_id")
    customer = payload.get("customer_details", {})
    username = customer.get("customer_id")
    amount = payload.get("order_amount")

    if not all([order_id, payment_status, username]):
        logger.error("Webhook rejected: missing mandatory fields")
        raise HTTPException(status_code=400, detail="Missing fields")

    # ----------------------------------------------------------------
    # ACCEPT ONLY SUCCESS
    # ----------------------------------------------------------------

    if payment_status not in ("SUCCESS", "PAID"):
        logger.info(
            f"Ignoring non-success payment: order={order_id}, status={payment_status}"
        )
        return {"status": "ignored"}

    # ----------------------------------------------------------------
    # RECORD PAYMENT (IDEMPOTENT)
    # ----------------------------------------------------------------

    record_payment(
        order_id=order_id,
        username=username,
        amount=amount,
        status="SUCCESS",
        payment_id=payment_id,
    )

    logger.info(f"✅ Payment verified via webhook: order={order_id}")

    return {"status": "ok"}
