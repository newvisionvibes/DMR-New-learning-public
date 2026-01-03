"""
BULLETPROOF AUTHENTICATION - PERMANENT FIX
Creates users_database.json with admin user on first run
Proper syntax with all closing braces
"""

import json
import os
from datetime import datetime
import streamlit as st


class UserManager:
    """Manages user accounts and authentication"""
    
    def __init__(self, users_db_file="users_database.json"):
        """Initialize with users database file"""
        self.users_db_file = users_db_file
        self.users = {}
        self.load_or_create_database()
    
    def load_or_create_database(self):
        """Load database or create if it doesn't exist"""
        
        # If database exists, load it
        if os.path.exists(self.users_db_file):
            try:
                with open(self.users_db_file, 'r') as f:
                    data = json.load(f)
                    print(f"✅ Loaded {self.users_db_file}")
                    
                    # Convert from JSON list format to dict format for easier access
                    for user in data.get("users", []):
                        self.users[user["username"]] = user
                    
                    # CHECK: if admin missing, add it
                    if "admin" not in self.users:
                        print("⚠️  Admin user missing! Adding default admin...")
                        self._create_default_admin()
                        self.save_database()
                    
                    return
            except Exception as e:
                print(f"⚠️  Error loading {self.users_db_file}: {e}")
        
        # If no database or error, create default
        print(f"📝 Creating new {self.users_db_file}...")
        self.users = {}
        self._create_default_admin()
        self.save_database()
    
    def _create_default_admin(self):
        """Create default admin user"""
        self.users["admin"] = {
            "username": "admin",
            "password": "Manu",
            "role": "admin",
            "email": "",
            "status": "active",
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": None
        }
    
    def save_database(self):
        """Save users to database file"""
        try:
            users_list = list(self.users.values())
            
            with open(self.users_db_file, 'w') as f:
                json.dump({"users": users_list}, f, indent=2)
            
            print(f"✅ Saved {self.users_db_file}")
        except Exception as e:
            print(f"❌ Error saving {self.users_db_file}: {e}")
    
    def verify_password(self, username, password):
        """
        Verify user password
        Returns True only if username exists, password matches, and account is active
        """
        if username not in self.users:
            print(f"❌ User '{username}' not found")
            return False
        
        user = self.users[username]
        
        if user.get("status") == "inactive":
            print(f"❌ User '{username}' is inactive")
            return False
        
        stored_password = user.get("password", "")
        if stored_password != password:
            print(f"❌ Wrong password for '{username}'")
            print(f"   Stored: '{stored_password}'")
            print(f"   Provided: '{password}'")
            return False
        
        print(f"✅ Login successful for '{username}'")
        return True
    
    def create_user(self, username, password, role="subscriber", email=""):
        """Create a new user account"""
        if username in self.users:
            return False, "User already exists"
        
        self.users[username] = {
            "username": username,
            "password": password,
            "role": role,
            "email": email,
            "status": "active",
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": None
        }
        
        self.save_database()
        return True, "User created successfully"
    
    def delete_user(self, username):
        """Delete a user account"""
        if username == "admin":
            return False, "Cannot delete admin account"
        
        if username in self.users:
            del self.users[username]
            self.save_database()
            return True, "User deleted"
        
        return False, "User not found"
    
    def get_all_users(self):
        """Get all users"""
        return self.users
    
    def update_user_status(self, username, status):
        """Update user status"""
        if username in self.users:
            self.users[username]["status"] = status
            self.save_database()
            return True
        return False
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if not self.verify_password(username, old_password):
            return False, "Incorrect password"
        
        self.users[username]["password"] = new_password
        self.save_database()
        return True, "Password changed successfully"


def login_page(user_manager):
    """Render login page"""
    
    
    
    st.markdown("# 🔐 Sector ETF RS Analyzer")
    st.markdown("### Professional Edition - Subscriber Access")
    st.divider()
    
    tab1, tab2 = st.tabs(["🔓 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", width="stretch", type="primary"):
            if username and password:
                if user_manager.verify_password(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_role = user_manager.users[username]["role"]
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("Please enter username and password")
        
        st.divider()
        
        st.info(
            "📝 **First Time Login?**\n\n"
            "Use credentials provided by your admin.\n\n"
            "💡 **Default Admin:** username=`admin`, password=`Manu`"
        )
    
    with tab2:
        st.subheader("Create New Account")
        st.info("📝 Contact your admin to create an account.")


def force_password_change_dialog(user_manager, username):
    """Show force password change dialog"""
    st.warning("🔐 **First Login - Password Change Required**")
    st.info("For security, you must change your password on first login.")
    
    st.divider()
    
    with st.form("force_password_change_form"):
        current_password = st.text_input(
            "Current Password",
            type="password"
        )
        
        new_password = st.text_input(
            "New Password",
            type="password"
        )
        
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password"
        )
        
        submitted = st.form_submit_button(
            "✅ Change Password & Continue",
            width="stretch",
            type="primary"
        )
        
        if submitted:
            if not new_password or not confirm_password:
                st.error("❌ Please fill all fields")
            elif new_password != confirm_password:
                st.error("❌ Passwords don't match")
            elif len(new_password) < 6:
                st.error("❌ Password min 6 characters")
            elif new_password == current_password:
                st.error("❌ New password must be different")
            else:
                ok, msg = user_manager.change_password(
                    username,
                    current_password,
                    new_password
                )
                
                if ok:
                    st.session_state.force_password_change = False
                    st.success("✅ Password changed!")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")
