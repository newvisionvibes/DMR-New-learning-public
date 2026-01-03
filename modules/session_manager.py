#!/usr/bin/env python3

"""
📋 SESSION MANAGER WITH PERSISTENT SESSION TRACKING
=====================================================

Enhanced version with 4 new keys for persistence tracking
Survives Streamlit reruns and app restarts

Version: 2.1 Enhanced
Date: 2026-01-02
Status: PRODUCTION READY ✅
"""

import streamlit as st
import os
from datetime import datetime
import pandas as pd


def init_session_state():
    """
    Initialize ALL session state variables
    Runs once at app startup
    
    ✅ ENHANCED: Added 4 new persistence tracking keys
    """
    
    defaults = {
        # ===== AUTHENTICATION (CRITICAL) =====
        "authenticated": False,
        "username": None,
        "user_role": None,
        "force_password_change": False,
        
        # ===== PERSISTENCE TRACKING (NEW) =====
        "persistence_check_done": False,  # Track if we checked for persistent session
        "last_activity": None,             # Last user activity timestamp
        "session_created": None,           # When session was created
        "session_expires": None,           # When session expires
        
        # ===== ANALYSIS DATA =====
        "analysis_results": None,
        "last_analysis_time": None,
        "etf_rs": None,
        "benchmark": "NIFTY 50",
        
        # ===== API CONNECTION (ADMIN ONLY) =====
        "admin_connected": False,
        "admin_connector": None,
        
        # ===== LEGACY COMPATIBILITY =====
        "connected": False,
        "connector": None,
        
        # ===== EMAIL CONFIGURATION =====
        "email_configured": False,
        
        # ===== UI STATE =====
        "show_etf_preview": False,
        "show_sector_preview": False,
        "show_comp_preview": False,
        "sector_newsletter_ready": False,
        "sector_newsletter_html": None,
        "etf_newsletter_ready": False,
        "etf_newsletter_html": None,
    }
    
    # Initialize all defaults
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # AUTO-LOAD PERSISTED DATA FROM ADMIN REFRESH
    if st.session_state.get("analysis_results") is None:
        analysis_data = load_persisted_analysis_data()
        if analysis_data is not None:
            st.session_state.analysis_results = analysis_data
            st.session_state.last_analysis_time = datetime.now()
    
    if st.session_state.get("etf_rs") is None:
        etf_data = load_persisted_etf_data()
        if etf_data is not None:
            st.session_state.etf_rs = etf_data


def load_persisted_analysis_data():
    """Load sector analysis data from persistent CSV file"""
    try:
        if os.path.exists("sector_analysis_data.csv"):
            df = pd.read_csv("sector_analysis_data.csv")
            return df
        return None
    except Exception as e:
        print(f"Error loading persisted analysis data: {e}")
        return None


def load_persisted_etf_data():
    """Load ETF data from persistent CSV file"""
    try:
        if os.path.exists("etf_rs_output.csv"):
            df = pd.read_csv("etf_rs_output.csv")
            return df
        return None
    except Exception as e:
        print(f"Error loading persisted ETF data: {e}")
        return None


def reset_session_state():
    """Reset all session state variables"""
    for key in st.session_state.keys():
        del st.session_state[key]
    
    init_session_state()


def update_session_activity():
    """Update last activity timestamp (called on every page load)"""
    if st.session_state.get("authenticated"):
        st.session_state.last_activity = datetime.now().isoformat()


def check_session_expiry() -> bool:
    """
    Check if current session has expired
    
    Returns:
        bool: True if session is still valid, False if expired
    """
    if not st.session_state.get("authenticated"):
        return False
    
    expires_at = st.session_state.get("session_expires")
    if not expires_at:
        return True  # No expiry set, assume valid
    
    try:
        from datetime import datetime as dt
        expiry_time = dt.fromisoformat(expires_at)
        return dt.now() < expiry_time
    except:
        return True  # If parsing fails, assume valid


def mark_session_as_active():
    """Mark current session as active (update timestamp and check expiry)"""
    update_session_activity()
    
    # Check if expired
    if not check_session_expiry():
        # Session expired
        st.session_state.authenticated = False
        st.session_state.username = None
        st.warning("⏱️ Your session has expired. Please log in again.")
        return False
    
    return True
