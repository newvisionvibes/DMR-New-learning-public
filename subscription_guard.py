from datetime import datetime
import pytz
import logging

from subscription_manager import SubscriptionManager
from persistent_sessions import clear_persistent_session

IST = pytz.timezone("Asia/Kolkata")
logger = logging.getLogger(__name__)


def enforce_subscription_or_logout(username: str, session_state):
    """
    Enforces subscription validity.
    If expired or missing → force logout immediately.
    """

    manager = SubscriptionManager()
    sub = manager.get_subscription(username)

    if not sub:
        logger.warning(f"No subscription found for {username}")
        _force_logout(username, session_state)
        return False

    expiry = sub.get("expires_at")
    if not expiry:
        logger.warning(f"No expiry found for {username}")
        _force_logout(username, session_state)
        return False

    try:
        expiry_dt = datetime.fromisoformat(expiry)
        now = datetime.now(IST)

        if now >= expiry_dt:
            logger.info(f"Subscription expired for {username}")
            manager.expire_subscription(username)
            _force_logout(username, session_state)
            return False

    except Exception as e:
        logger.error(f"Expiry check failed for {username}: {e}")
        _force_logout(username, session_state)
        return False

    return True


def _force_logout(username, session_state):
    """
    Clears Streamlit session + persistent session
    """
    try:
        clear_persistent_session(username)
    except Exception:
        pass

    for key in list(session_state.keys()):
        del session_state[key]

    session_state["authenticated"] = False
