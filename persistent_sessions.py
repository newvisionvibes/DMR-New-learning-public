# modules/persistent_sessions.py
# ============================================================
# PERSISTENT SESSION MANAGER
# Stores app login sessions + AngelOne tokens to JSON
# Survives Fly restarts, VM switches, and deploys
# ============================================================

import streamlit as st
import json
import os
from datetime import datetime, timedelta
import hashlib
import logging

logger = logging.getLogger(__name__)

SESSION_DB = "persistent_sessions.json"
ANGELONE_TOKENS_DB = "angelone_tokens.json"

# ============================================================
# Session Management
# ============================================================

def get_session_id():
    """Generate stable session ID from username + Streamlit user agent"""
    username = st.session_state.get('username', 'guest')
    # Use Streamlit version + username for stable fingerprint
    fingerprint = hashlib.md5(f"{username}_{st.__version__}".encode()).hexdigest()[:16]
    return fingerprint

def load_persistent_session(username):
    """Load persistent session from JSON file"""
    if not os.path.exists(SESSION_DB):
        return None
    
    try:
        with open(SESSION_DB, 'r') as f:
            sessions = json.load(f)
        
        if username not in sessions:
            return None
        
        session_id = get_session_id()
        session_data = sessions.get(username, {}).get(session_id)
        
        if not session_data:
            return None
        
        # Check expiry
        expires_at = datetime.fromisoformat(session_data.get('expires', datetime.now().isoformat()))
        if expires_at < datetime.now():
            logger.warning(f"Session for {username} has expired")
            return None
        
        return session_data
    
    except Exception as e:
        logger.error(f"Error loading persistent session: {e}")
        return None

def save_persistent_session(username, role, user_id=None, expiry_days=7):
    """Save session to persistent JSON file (expires in N days)"""
    session_id = get_session_id()
    expiry = (datetime.now() + timedelta(days=expiry_days)).isoformat()
    
    session_data = {
        'username': username,
        'role': role,
        'user_id': user_id,
        'created': datetime.now().isoformat(),
        'expires': expiry,
        'last_activity': datetime.now().isoformat()
    }
    
    try:
        # Load existing sessions
        if os.path.exists(SESSION_DB):
            with open(SESSION_DB, 'r') as f:
                sessions = json.load(f)
        else:
            sessions = {}
        
        # Add/update user session
        if username not in sessions:
            sessions[username] = {}
        sessions[username][session_id] = session_data
        
        # Write back
        with open(SESSION_DB, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        logger.info(f"Persistent session saved for {username}")
        return True
    
    except Exception as e:
        logger.error(f"Error saving persistent session: {e}")
        return False

def clear_persistent_session(username):
    """Remove session on logout"""
    if not os.path.exists(SESSION_DB):
        return True
    
    try:
        with open(SESSION_DB, 'r') as f:
            sessions = json.load(f)
        
        if username in sessions:
            del sessions[username]
            with open(SESSION_DB, 'w') as f:
                json.dump(sessions, f, indent=2)
            logger.info(f"Persistent session cleared for {username}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error clearing persistent session: {e}")
        return False

def update_session_activity(username):
    """Update last activity timestamp"""
    if not os.path.exists(SESSION_DB):
        return False
    
    try:
        with open(SESSION_DB, 'r') as f:
            sessions = json.load(f)
        
        session_id = get_session_id()
        if username in sessions and session_id in sessions[username]:
            sessions[username][session_id]['last_activity'] = datetime.now().isoformat()
            with open(SESSION_DB, 'w') as f:
                json.dump(sessions, f, indent=2)
            return True
        
        return False
    
    except Exception as e:
        logger.error(f"Error updating session activity: {e}")
        return False

# ============================================================
# AngelOne Token Management
# ============================================================

def save_angelone_token(username, api_key, client_code, password, totp, token_expiry_minutes=1440):
    """Save AngelOne credentials + token expiry to persistent storage"""
    token_data = {
        'username': username,
        'api_key': api_key,
        'client_code': client_code,
        'password': password,
        'totp': totp,
        'created': datetime.now().isoformat(),
        'expires': (datetime.now() + timedelta(minutes=token_expiry_minutes)).isoformat(),
        'last_used': datetime.now().isoformat()
    }
    
    try:
        # Load existing tokens
        if os.path.exists(ANGELONE_TOKENS_DB):
            with open(ANGELONE_TOKENS_DB, 'r') as f:
                tokens = json.load(f)
        else:
            tokens = {}
        
        # Save token for this user
        tokens[username] = token_data
        
        with open(ANGELONE_TOKENS_DB, 'w') as f:
            json.dump(tokens, f, indent=2)
        
        logger.info(f"AngelOne token saved for {username}, expires in {token_expiry_minutes} minutes")
        return True
    
    except Exception as e:
        logger.error(f"Error saving AngelOne token: {e}")
        return False

def load_angelone_token(username):
    """Load saved AngelOne credentials if still valid"""
    if not os.path.exists(ANGELONE_TOKENS_DB):
        return None
    
    try:
        with open(ANGELONE_TOKENS_DB, 'r') as f:
            tokens = json.load(f)
        
        if username not in tokens:
            return None
        
        token_data = tokens[username]
        
        # Check expiry
        expires_at = datetime.fromisoformat(token_data.get('expires', datetime.now().isoformat()))
        if expires_at < datetime.now():
            logger.warning(f"AngelOne token for {username} has expired")
            return None
        
        # Update last_used
        token_data['last_used'] = datetime.now().isoformat()
        with open(ANGELONE_TOKENS_DB, 'w') as f:
            json.dump(tokens, f, indent=2)
        
        logger.info(f"AngelOne token loaded for {username}")
        return token_data
    
    except Exception as e:
        logger.error(f"Error loading AngelOne token: {e}")
        return None

def clear_angelone_token(username):
    """Remove AngelOne token on logout or expiry"""
    if not os.path.exists(ANGELONE_TOKENS_DB):
        return True
    
    try:
        with open(ANGELONE_TOKENS_DB, 'r') as f:
            tokens = json.load(f)
        
        if username in tokens:
            del tokens[username]
            with open(ANGELONE_TOKENS_DB, 'w') as f:
                json.dump(tokens, f, indent=2)
            logger.info(f"AngelOne token cleared for {username}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error clearing AngelOne token: {e}")
        return False

def is_angelone_token_valid(username):
    """Check if AngelOne token exists and is not expired"""
    token_data = load_angelone_token(username)
    return token_data is not None
