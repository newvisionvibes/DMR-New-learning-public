# ============================================================================
# FIXED header.py - WITH LIVE TIMESTAMP DISPLAY
# ============================================================================

"""
Header Components Module - FIXED VERSION
Renders application header with LIVE updating timestamp
"""

import streamlit as st
import time
from datetime import datetime
import pytz

# Define IST timezone
IST = pytz.timezone("Asia/Kolkata")

def render_header_with_timestamp():
    """
    Render application header with LIVE market status and timestamp
    
    This replaces the old header that showed static timestamp.
    Now shows:
    - Title & description (left)
    - Market status badge (center) 
    - LIVE timestamp that updates on every page reload (right)
    """
    
    # Create columns: Title | Spacer | Market Status | Timestamp
    col_title, col_spacer, col_status, col_time = st.columns([1.5, 1.5, 1, 1.2])
    
    with col_title:
        st.markdown("# 📊 D's Sector ETF RS Analyzer")
        st.markdown("**Market Data For Study Purpose** - Educational Edition V7")
    
    # Get LIVE timestamp on EVERY page reload (not cached!)
    current_time_ist = datetime.now(IST)
    is_market_open = (
        current_time_ist.weekday() < 5 and  # Mon-Fri
        current_time_ist.time() >= datetime.min.time().replace(hour=9, minute=15) and
        current_time_ist.time() <= datetime.min.time().replace(hour=15, minute=30)
    )
    
    with col_status:
        if is_market_open:
            st.markdown("### 🟢 **Market OPEN**")
        else:
            st.markdown("### 🔵 **Market CLOSED**")
    
    with col_time:
        # ✅ THIS IS THE FIX: Call datetime.now() EVERY render, not cached!
        formatted_time = current_time_ist.strftime("%Y-%m-%d %H:%M:%S IST")
        st.markdown(f"**🕐 {formatted_time}**")
    
    st.divider()


def render_header():
    """Render application header (original function)"""
    st.markdown("# 📊 D's Sector ETF RS Analyzer - Educational Edition")
    st.markdown("### 📚 Market Data For Study Purpose")
    st.caption("Sectors • ETFs • Strategy Classification • Educational Newsletter Distribution")
    st.divider()


def render_user_header():
    """Render user info and logout button"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.caption(
            f"👤 **Logged in as:** {st.session_state.username} "
            f"({st.session_state.user_role.capitalize()})"
        )
    
    with col3:
        if st.button("🚪 Logout", width="stretch", key="main_logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_role = None
            st.session_state.force_password_change = False
            st.session_state.admin_connected = False
            st.session_state.admin_connector = None
            st.session_state.connected = False
            st.session_state.connector = None
            st.success("✅ Logged out successfully!")
            time.sleep(1)
            st.rerun()
