from fastapi import APIRouter, Request
from payments_store import record_payment

router = APIRouter()

@router.post("/webhook/cashfree")
async def cashfree_webhook(request: Request):
    payload = await request.json()

    order_id = payload.get("order_id")
    status = payload.get("order_status")
    payment_id = payload.get("payment_id")
    username = payload.get("customer_details", {}).get("customer_id")

    if status == "PAID":
        record_payment(
            order_id=order_id,
            username=username,
            amount=999,
            status="SUCCESS",
            payment_id=payment_id,
        )

    return {"status": "ok"}
