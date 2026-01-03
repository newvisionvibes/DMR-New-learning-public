import json
import os
import threading
from datetime import datetime

LOCK = threading.Lock()

USERS_FILE = "users_database.json"
SUBSCRIPTIONS_FILE = "subscriptions_database.json"


class UserStore:
    def __init__(self):
        self._ensure_files()

    # ------------------ Internal ------------------

    def _ensure_files(self):
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w") as f:
                json.dump([], f, indent=2)

        if not os.path.exists(SUBSCRIPTIONS_FILE):
            with open(SUBSCRIPTIONS_FILE, "w") as f:
                json.dump([], f, indent=2)

    def _load(self, path):
        with LOCK:
            with open(path, "r") as f:
                return json.load(f)

    def _save(self, path, data):
        with LOCK:
            with open(path, "w") as f:
                json.dump(data, f, indent=2)

    # ✅ BACKWARD-COMPATIBILITY SHIM (CRITICAL FIX)
    def _load_users(self):
        """
        Compatibility method.
        Older code expects _load_users().
        Users are stored as a LIST in JSON.
        """
        return self._load(USERS_FILE)

    # ------------------ Users ------------------

    def get_user(self, username):
        users = self._load_users()
        return next((u for u in users if u["username"] == username), None)

    def get_all_users(self):
        # ✅ users are already a list
        return self._load_users()

    def set_status(self, user_id, status):
        users = self._load_users()
        for u in users:
            if u["id"] == user_id:
                u["status"] = status
        self._save(USERS_FILE, users)

    def change_password(self, user_id, new_password):
        users = self._load_users()
        for u in users:
            if u["id"] == user_id:
                u["password"] = new_password
        self._save(USERS_FILE, users)

    def create_user(self, username, password, role, email=None):
        users = self._load_users()

        if any(u["username"] == username for u in users):
            return False, "Username already exists"

        new_user = {
            "id": max([u["id"] for u in users], default=0) + 1,
            "username": username,
            "password": password,
            "role": role,
            "email": email,
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        }

        users.append(new_user)
        self._save(USERS_FILE, users)

        if role == "subscriber":
            self.ensure_subscription(new_user["id"])

        return True, "User created successfully"

    # ------------------ Subscriptions ------------------

    def ensure_subscription(self, user_id):
        subs = self._load(SUBSCRIPTIONS_FILE)

        if not any(s["user_id"] == user_id for s in subs):
            subs.append({
                "user_id": user_id,
                "active": True,
                "plan": "basic",
                "created_at": datetime.utcnow().isoformat()
            })

        self._save(SUBSCRIPTIONS_FILE, subs)

    def get_active_subscription(self, user_id):
        subs = self._load(SUBSCRIPTIONS_FILE)
        return next(
            (s for s in subs if s["user_id"] == user_id and s["active"]),
            None
        )
