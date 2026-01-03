import json
import os
from datetime import datetime, timedelta
import pytz
import threading

IST = pytz.timezone("Asia/Kolkata")
LOCK = threading.Lock()

SUBSCRIPTION_FILE = "data/subscriptions.json"


class SubscriptionManager:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(SUBSCRIPTION_FILE):
            self._init_file()

    def _init_file(self):
        with open(SUBSCRIPTION_FILE, "w") as f:
            json.dump(
                {
                    "schema_version": "1.0",
                    "plans": {},
                    "users": {}
                },
                f,
                indent=2,
            )

    def _load(self):
        with LOCK:
            with open(SUBSCRIPTION_FILE, "r") as f:
                return json.load(f)

    def _save(self, data):
        with LOCK:
            tmp = SUBSCRIPTION_FILE + ".tmp"
            with open(tmp, "w") as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, SUBSCRIPTION_FILE)

    # ---------------- CORE API ---------------- #

    def grant_subscription(self, username, plan="premium", days=30):
        data = self._load()
        expiry = datetime.now(IST) + timedelta(days=days)

        data["users"][username] = {
            "plan": plan,
            "start": datetime.now(IST).isoformat(),
            "expiry": expiry.isoformat(),
            "active": True,
        }

        self._save(data)

    def revoke_subscription(self, username):
        data = self._load()
        if username in data["users"]:
            data["users"][username]["active"] = False
            self._save(data)

    def get_subscription(self, username):
        data = self._load()
        sub = data["users"].get(username)
        if not sub:
            return None

        expiry = datetime.fromisoformat(sub["expiry"])
        if expiry < datetime.now(IST):
            sub["active"] = False
            self._save(data)

        return sub

    def has_active_subscription(self, username):
        sub = self.get_subscription(username)
        return bool(sub and sub.get("active"))
