"""
Payment handling for successful/failed transactions
Includes webhook processing and callback handling
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional
import streamlit as st
from cashfree_integration import (
    create_subscription,
    generate_invoice,
    CashfreePaymentGateway
)

def handle_payment_success(
    user_id: int,
    username: str,
    email: str,
    plan: str,
    amount: float,
    payment_id: str
) -> bool:
    """
    Handle successful payment
    
    Args:
        user_id: User ID
        username: Username
        email: Email
        plan: Subscription plan
        amount: Amount paid
        payment_id: Cashfree payment ID
    
    Returns:
        Success status
    """
    
    # Create subscription
    success, error = create_subscription(
        user_id=user_id,
        plan=plan,
        payment_id=payment_id,
        amount=amount,
        payment_method="cashfree"
    )
    
    if not success:
        print(f"Subscription creation failed: {error}")
        return False
    
    # Generate invoice
    invoice_html = generate_invoice(
        user_id=user_id,
        username=username,
        email=email,
        plan=plan,
        amount=amount,
        payment_id=payment_id
    )
    
    # Save invoice (optional)
    invoice_file = f"invoices/{username}_{payment_id}.html"
    os.makedirs("invoices", exist_ok=True)
    
    try:
        with open(invoice_file, 'w') as f:
            f.write(invoice_html)
    except Exception as e:
        print(f"Invoice save failed: {e}")
    
    # Log payment
    log_payment(
        user_id=user_id,
        username=username,
        payment_id=payment_id,
        amount=amount,
        status="SUCCESS"
    )
    
    return True


def handle_payment_failure(
    user_id: int,
    username: str,
    payment_id: str,
    error_message: str
) -> None:
    """Handle payment failure"""
    
    log_payment(
        user_id=user_id,
        username=username,
        payment_id=payment_id,
        amount=0,
        status="FAILED",
        error=error_message
    )


def log_payment(
    user_id: int,
    username: str,
    payment_id: str,
    amount: float,
    status: str,
    error: Optional[str] = None
) -> None:
    """Log payment transaction"""
    
    log_file = "payment_logs.json"
    
    # Load existing logs
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = {"payments": []}
    
    # Add new log
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": user_id,
        "username": username,
        "payment_id": payment_id,
        "amount": amount,
        "status": status,
        "error": error
    }
    
    logs["payments"].append(log_entry)
    
    # Save logs
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)


def verify_and_activate_subscription(
    order_id: str,
    payment_id: str,
    user_id: int,
    username: str,
    email: str,
    plan: str,
    amount: float
) -> Dict:
    """
    Verify payment and activate subscription
    
    Returns:
        Status dictionary with success/error info
    """
    
    try:
        # Initialize Cashfree gateway
        gateway = CashfreePaymentGateway()
        
        # Verify payment
        success, error, payment_data = gateway.verify_payment(
            order_id=order_id,
            payment_id=payment_id
        )
        
        if not success:
            handle_payment_failure(
                user_id=user_id,
                username=username,
                payment_id=payment_id,
                error_message=error
            )
            return {
                "success": False,
                "message": f"Payment verification failed: {error}"
            }
        
        # Create subscription
        if handle_payment_success(
            user_id=user_id,
            username=username,
            email=email,
            plan=plan,
            amount=amount,
            payment_id=payment_id
        ):
            return {
                "success": True,
                "message": "✅ Payment successful! Subscription activated.",
                "order_id": order_id,
                "payment_id": payment_id
            }
        else:
            return {
                "success": False,
                "message": "Payment verified but subscription creation failed"
            }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }
