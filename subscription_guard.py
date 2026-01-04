"""
SUBSCRIPTION GUARD – PHASE 5.1.3
--------------------------------
Single enforcement point for premium access.

RULE:
Access is allowed ONLY if:
- User is authenticated
- AND payment is confirmed via Cashfree webhook
"""

import logging
from typing import Optional

from payments_store import has_successful_payment
from user_store import UserStore

logger = logging.getLogger(__name__)


def enforce_subscription_or_logout(
    username: str,
    session_state,
    *,
    strict: bool = True
) -> bool:
    """
    Enforce premium subscription access.

    Returns:
        True  -> Access allowed
        False -> User logged out / blocked

    strict=True:
        - Immediately logs out user if payment invalid
    strict=False:
        - Allows caller to handle UI fallback
    """

    # ------------------------------------------------------------------
    # 1️⃣ BASIC SESSION VALIDATION
    # ------------------------------------------------------------------

    if not session_state.get("authenticated"):
        logger.warning("Subscription guard: unauthenticated access attempt")
        return False

    if not username:
        logger.warning("Subscription guard: missing username")
        return False

    # ------------------------------------------------------------------
    # 2️⃣ ADMIN BYPASS (INTENTIONAL)
    # ------------------------------------------------------------------

    if session_state.get("user_role") == "admin":
        logger.info("Subscription guard: admin bypass granted")
        session_state.has_active_subscription = True
        return True

    # ------------------------------------------------------------------
    # 3️⃣ PAYMENT VERIFICATION (SOURCE OF TRUTH)
    # ------------------------------------------------------------------

    payment_ok = has_successful_payment(username)

    if not payment_ok:
        logger.warning(
            f"Subscription guard: payment not verified for user={username}"
        )

        session_state.has_active_subscription = False

        if strict:
            _logout_user(session_state)

        return False

    # ------------------------------------------------------------------
    # 4️⃣ FINALIZE SESSION STATE
    # ------------------------------------------------------------------

    session_state.has_active_subscription = True
    logger.info(f"Subscription guard: access granted to {username}")
    return True


# ----------------------------------------------------------------------
# INTERNAL HELPERS
# ----------------------------------------------------------------------

def _logout_user(session_state):
    """
    Centralized logout logic.
    Ensures clean session reset.
    """
    try:
        from persistent_sessions import clear_persistent_session

        username = session_state.get("username")
        if username:
            clear_persistent_session(username)
    except Exception as e:
        logger.warning(f"Failed to clear persistent session: {e}")

    # Hard reset Streamlit session
    for key in list(session_state.keys()):
        del session_state[key]

    session_state["authenticated"] = False
    session_state["has_active_subscription"] = False
