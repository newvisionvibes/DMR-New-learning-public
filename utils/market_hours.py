"""
Market Hours Utility
Handles NSE market open / close logic (IST)
"""

from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")


def is_market_open(now=None):
    if now is None:
        now = datetime.now(IST)

    # Weekend
    if now.weekday() >= 5:
        return False

    open_time = now.replace(hour=9, minute=15, second=0, microsecond=0)
    close_time = now.replace(hour=15, minute=30, second=0, microsecond=0)

    return open_time <= now <= close_time
