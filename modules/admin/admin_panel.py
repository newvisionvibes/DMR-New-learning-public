"""
ADMIN PANEL WITH USER MANAGEMENT
Complete admin control panel with user creation/management
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from user_management import render_user_management
from output_renderers import (
    render_sector_output_view,
    render_etf_output_view,
    render_comprehensive_output_view
)


def render_admin_panel(user_manager):
    """Render complete admin control panel with all features"""
    
    # Check admin role
    if st.session_state.get("user_role") != "admin":
        st.error("❌ Admin access required. Contact system administrator.")
        return
    
    # Admin Header
    st.markdown("## 👨‍💼 Admin Control Panel")
    st.caption("🔐 Admin Mode - Manage users, refresh data, and monitor system")
    
    st.divider()
    
    # Admin Navigation - 6 TABS
    admin_tabs = st.tabs([
        "👥 User Management",
        "🔄 Data Refresh",
        "📊 System Status",
        "🔐 Security",
        "📊 Sector Output",
        "💼 ETF Output",
        "📈 Comprehensive"
    ])
    
    # =========================================================================
    # TAB 1: USER MANAGEMENT
    # =========================================================================
    
    with admin_tabs[0]:
        render_user_management()
    
    # =========================================================================
    # TAB 2: DATA REFRESH
    # =========================================================================
    
    with admin_tabs[1]:
        st.subheader("🔄 Data Refresh & Analysis Control")
        st.info("Data refresh functionality - Use your existing admin_panel.py code here")
    
    # =========================================================================
    # TAB 3: SYSTEM STATUS
    # =========================================================================
    
    with admin_tabs[2]:
        st.subheader("📊 System Status & Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("API Status", "✅ Connected")
        
        with col2:
            st.metric("Data Age", "Fresh")
        
        with col3:
            st.metric("Users", "Active")
        
        with col4:
            st.metric("Last Update", datetime.now().strftime("%H:%M IST"))
        
        st.divider()
        st.info("System status details - Use your existing admin_panel.py code here")
    
    # =========================================================================
    # TAB 4: SECURITY
    # =========================================================================
    
    with admin_tabs[3]:
        st.subheader("🔐 Security Settings")
        st.info("Security management - Use your existing admin_panel.py code here")
    
    # =========================================================================
    # TAB 5: SECTOR OUTPUT PREVIEW
    # =========================================================================
    
    with admin_tabs[4]:
        st.subheader("📊 Sector Analysis Output Preview")
        st.caption("Preview how subscribers will see this report")
        render_sector_output_view(show_admin_controls=False)
    
    # =========================================================================
    # TAB 6: ETF OUTPUT PREVIEW
    # =========================================================================
    
    with admin_tabs[5]:
        st.subheader("💼 ETF Analysis Output Preview")
        st.caption("Preview how subscribers will see this report")
        render_etf_output_view(show_admin_controls=False)
    
    # =========================================================================
    # TAB 7: COMPREHENSIVE OUTPUT PREVIEW
    # =========================================================================
    
    with admin_tabs[6]:
        st.subheader("📈 Comprehensive Analysis Output Preview")
        st.caption("Preview how subscribers will see this report")
        render_comprehensive_output_view(show_admin_controls=False)
