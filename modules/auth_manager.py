"""
Authentication Manager Module
Provides login protection decorator for secure pages
Location: modules/auth_manager.py
Status: Production Ready
Updated: 2026-01-01
"""

import streamlit as st
import logging

logger = logging.getLogger(__name__)


def require_login(func):
    """
    ✅ DECORATOR: Protects pages that require user authentication
    
    Usage:
        @require_login
        def my_protected_page():
            st.write("Only logged-in users see this")
    
    Features:
        - Checks st.session_state.authenticated
        - Shows warning if not logged in
        - Prevents unauthorized access
        - No additional setup needed
    
    Args:
        func: Function to decorate (typically a page/tab renderer)
    
    Returns:
        Wrapper function with authentication check
    """
    def wrapper(*args, **kwargs):
        # Check if user is authenticated
        if not st.session_state.get("authenticated", False):
            # User not logged in - show warning and stop
            st.warning("⚠️ Please login first to access this page.")
            st.info("📝 Use the login form on the landing page to sign in.")
            logger.info("Blocked unauthenticated access to protected page")
            st.stop()
        
        # User authenticated - execute the original function
        logger.info(f"User {st.session_state.get('username', 'Unknown')} accessing protected page")
        return func(*args, **kwargs)
    
    # Preserve function metadata
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def get_user_role():
    """
    Get the current user's role from session state
    
    Returns:
        str: User role ('admin', 'subscriber', None)
    """
    return st.session_state.get("user_role", None)


def is_admin():
    """
    Check if current user is admin
    
    Returns:
        bool: True if user is admin, False otherwise
    """
    return get_user_role() == "admin"


def is_authenticated():
    """
    Check if user is currently authenticated
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    return st.session_state.get("authenticated", False)
