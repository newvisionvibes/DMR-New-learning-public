from fastapi import FastAPI, Request, HTTPException
import logging

from payment_processor import PaymentProcessor

app = FastAPI()
processor = PaymentProcessor()
logger = logging.getLogger(__name__)


@app.post("/webhook/cashfree")
async def cashfree_webhook(request: Request):
    payload = await request.json()

    try:
        event = payload.get("event")
        data = payload.get("data", {})

        if event != "PAYMENT_SUCCESS":
            return {"status": "ignored"}

        order_id = data.get("order_id")
        username = data.get("customer_details", {}).get("customer_id")

        if not order_id or not username:
            raise HTTPException(status_code=400, detail="Invalid payload")

        processor.record_payment({
            "order_id": order_id,
            "username": username,
            "amount": data.get("order_amount"),
            "status": "SUCCESS",
            "payment_id": data.get("cf_payment_id"),
        })

        return {"status": "processed"}

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Webhook failed")
