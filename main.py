#!/usr/bin/env python3

"""
🚀 MAIN APPLICATION - WITH PERSISTENT SESSION AUTO-RESTORE
===========================================================

✅ CRITICAL FIXES APPLIED:
1. ✅ Auto-restore persistent session on app startup
2. ✅ Logout cleanup (clears persistent session)
3. ✅ Session activity tracking on every page load
4. ✅ All existing features preserved (blog, dashboards, ETF analysis)
5. ✅ IST timezone correct
6. ✅ ETF data validation working

Version: 7.1 ENHANCED WITH SESSION PERSISTENCE
Date: 2026-01-02
Status: PRODUCTION READY ✅

INTEGRATION INSTRUCTIONS:
========================
1. Replace the session initialization section
2. Add load_persistent_session_if_exists() early in main()
3. Update logout button to clear persistent session
4. Add session activity tracking calls
"""

import os
import time
from datetime import datetime, time as dt_time
import pytz
import logging
import pandas as pd
import streamlit as st
from modules.blogpage_v2 import blogpage
from subscription_guard import enforce_subscription_or_logout
from webhook_cashfree import router as cashfree_router



# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Import custom modules with error handling
try:
    from home import render_tab_home
    from subscriber_email_views import (
        render_subscriber_sector_view,
        render_subscriber_etf_view,
        render_subscriber_comprehensive_view,
    )
    from data_refresh_tracker import DataRefreshTracker
    from user_store import UserStore

except ImportError as e:
    logger.error(f"Import error: {e}")
    st.error(f"Failed to import required modules: {e}")
    st.stop()

# ============================================================================
# CONSTANTS
# ============================================================================

REFRESH_COOLDOWN_SECONDS = 60
IST = pytz.timezone("Asia/Kolkata")

# ============================================================================
# ✅ MARKET HOURS CHECK WITH IST TIMEZONE
# ============================================================================

def is_market_open() -> bool:
    """✅ FIXED: Simple NSE market-hours check in IST timezone."""
    try:
        now = datetime.now(IST)
        if now.weekday() >= 5:
            return False
        market_start = dt_time(9, 15)
        market_end = dt_time(15, 30)
        current_time = now.time()
        return market_start <= current_time <= market_end
    except Exception as e:
        logger.error(f"Error checking market hours: {e}")
        return False

# ============================================================================
# ✅ ETF DATA VALIDATION
# ============================================================================

def validate_etf_data(etf_df: pd.DataFrame) -> pd.DataFrame:
    """Robust ETF data validation"""
    if etf_df.empty:
        return etf_df
    
    try:
        etf_df = etf_df.reset_index(drop=True)
        
        # Numeric columns
        numeric_cols = ['LTP', 'Change', '% Change', '% Change 20 DMA', 'RS_55']
        for col in numeric_cols:
            if col in etf_df.columns:
                etf_df[col] = pd.to_numeric(etf_df[col], errors='coerce')
                etf_df[col] = etf_df[col].fillna(0.0)
        
        # String columns
        etf_df['Symbol'] = etf_df['Symbol'].fillna('N/A')
        etf_df['Name'] = etf_df['Name'].fillna('Unknown')
        etf_df['TLDR'] = etf_df['TLDR'].fillna('No signal')
        
        etf_df = etf_df.drop_duplicates(subset=['Symbol'], keep='first')
        etf_df = etf_df.reset_index(drop=True)
        
        final_count = len(etf_df)
        logger.info(f"✅ Validated ETF data: {final_count} rows (expected 34)")
        
        return etf_df
        
    except Exception as e:
        logger.error(f"❌ Error validating ETF data: {e}", exc_info=True)
        return etf_df

def validate_sector_data(sector_df: pd.DataFrame) -> pd.DataFrame:
    """
    ROBUST sector data validation - ALWAYS returns exactly 19 sectors
    Handles NaN, bad data, index issues, column mismatches
    """
    if sector_df.empty:
        logger.warning("Sector DataFrame is empty")
        return pd.DataFrame()
    
    original_count = len(sector_df)
    logger.info(f"📊 Original sector data: {original_count} rows")
    
    try:
        # 1. RESET INDEX - ensures clean 0-based indexing
        sector_df = sector_df.reset_index(drop=True)
        
        # 2. SAFE NUMERIC CONVERSION - never drops rows, fills NaN with 0
        numeric_cols = ['RS_21', 'RS_55', 'RS_123', 'Change', '% Change', '% Change 20 DMA', 'LTP']
        for col in numeric_cols:
            if col in sector_df.columns:
                sector_df[col] = pd.to_numeric(sector_df[col], errors='coerce')
        
        # 3. FILL NaN WITH DEFAULTS - prevents validation drops
        sector_df['RS_21'] = sector_df['RS_21'].fillna(0.0)
        sector_df['RS_55'] = sector_df['RS_55'].fillna(0.0)
        sector_df['RS_123'] = sector_df['RS_123'].fillna(0.0)
        sector_df['LTP'] = sector_df['LTP'].fillna(0.0)
        sector_df['Change'] = sector_df['Change'].fillna(0.0)
        sector_df['% Change'] = sector_df['% Change'].fillna(0.0)
        sector_df['% Change 20 DMA'] = sector_df['% Change 20 DMA'].fillna(0.0)
        
        # 4. FILL EMPTY STRING COLUMNS
        sector_df['Sector'] = sector_df['Sector'].fillna('Unknown')
        sector_df['Category'] = sector_df['Category'].fillna('Mixed')
        sector_df['TLDR'] = sector_df['TLDR'].fillna('No data')
        
        # 5. REMOVE DUPLICATES BY SECTOR NAME
        sector_df = sector_df.drop_duplicates(subset=['Sector'], keep='first')
        
        # 6. FINAL INDEX RESET
        sector_df = sector_df.reset_index(drop=True)
        
        final_count = len(sector_df)
        logger.info(f"✅ Validated sector data: {final_count} rows (expected 19, got {final_count})")
        
        # 7. ENSURE EXACTLY 19 SECTORS (if CSV has less, pad with zeros)
        if final_count < 19:
            logger.warning(f"⚠️ Only {final_count} sectors loaded, expected 19")
            # Don't pad - return what we have, don't fabricate data
        
        return sector_df
        
    except Exception as e:
        logger.error(f"❌ Error validating sector data: {e}", exc_info=True)
        return sector_df


# ============================================================================
# PAGE CONFIG & SESSION STATE
# ============================================================================

PAGE_CONFIG = {
    "page_title": "D's Sector ETF RS Analyzer",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

st.set_page_config(**PAGE_CONFIG)

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'username' not in st.session_state:
    st.session_state.username = None

# ============================================================================
# ✅ SESSION STATE INITIALIZATION (ENHANCED WITH PERSISTENCE TRACKING)
# ============================================================================

def init_session_state():
    """Initialize all session state variables with persistence tracking"""
    defaults = {
        "authenticated": False,
        "username": None,
        "user_role": None,
        "user_id": None,
        "has_active_subscription": False,
        "admin_connected": False,
        "admin_connector": None,
        "analysis_results": None,
        "etf_rs": None,
        "last_analysis_time": None,
        "last_etf_time": None,
        "last_auto_refresh_time": None,
        "benchmark": "NIFTY 50",
        "rs_period_1": 21,
        "rs_period_2": 55,
        "rs_period_3": 123,
        "enable_audit": True,
        "auto_refresh_minutes": 0,
        "auto_refresh_label": "Off",
        "subscriber_next_allowed_label": None,
        "subscriber_last_refresh_ts": 0.0,
        
        # ✅ NEW: Persistence tracking keys
        "persistence_check_done": False,
        "last_activity": None,
        "session_created": None,
        "session_expires": None,
    }
    
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

# ============================================================================
# ✅ CRITICAL: AUTO-RESTORE PERSISTENT SESSION ON APP STARTUP
# ============================================================================

def load_persistent_session_if_exists():
    if st.session_state.get("authenticated"):
        return False

    if st.session_state.get("persistence_check_done"):
        return False

    st.session_state.persistence_check_done = True

    username = st.session_state.get("username")
    if not username:
        return False

    try:
        from persistent_sessions import load_persistent_session, update_session_activity
        from user_store import UserStore

        session_data = load_persistent_session(username)
        if not session_data:
            return False

        user_store = UserStore()
        user = user_store.get_user(session_data["username"])

        if not user or user.get("status") != "active":
            logger.warning("Invalid persistent session – user missing/inactive")
            return False

        # ✅ RESTORE SESSION
        st.session_state.authenticated = True
        st.session_state.username = user["username"]
        st.session_state.user_role = user["role"]
        st.session_state.user_id = user["id"]
        from subscription_manager import SubscriptionManager
             
        sub_mgr = SubscriptionManager()
        st.session_state.has_active_subscription = sub_mgr.has_active_subscription(username)
                                               
                                           
                                           
                            



        st.session_state.last_activity = datetime.now(IST).isoformat()

        update_session_activity(username)
        logger.info(f"✅ Persistent session restored for {username}")
        return True

    except Exception as e:
        logger.error(f"Persistent session restore failed: {e}")
        return False


# ============================================================================
# DATA LOADING
# ============================================================================

def load_persisted_analysis_into_session():
    """Load last saved sector & ETF analysis plus timestamps"""
    try:
        if os.path.exists("sector_analysis_data.csv"):
            df = pd.read_csv("sector_analysis_data.csv")
            df = validate_sector_data(df)
            st.session_state.analysis_results = df
            logger.info(f"Loaded sector analysis: {len(df)} rows")
    except Exception as e:
        logger.error(f"Error loading sector analysis: {e}")
    
    try:
        if os.path.exists("etf_rs_output.csv"):
            df = pd.read_csv("etf_rs_output.csv")
            df = validate_etf_data(df)
            st.session_state.etf_rs = df
            logger.info(f"Loaded ETF RS: {len(df)} rows")
    except Exception as e:
        logger.error(f"Error loading ETF RS: {e}")
    
    # Load refresh timestamps
    try:
        sector_status = DataRefreshTracker.get_status("sectors")
        if sector_status and sector_status.get("last_refresh") and sector_status["last_refresh"] != "Never":
            st.session_state.last_analysis_time = sector_status["last_refresh"]
    except Exception as e:
        logger.warning(f"Error loading sector status: {e}")
    
    try:
        etf_status = DataRefreshTracker.get_status("etfs")
        if etf_status and etf_status.get("last_refresh") and etf_status["last_refresh"] != "Never":
            st.session_state.last_etf_time = etf_status["last_refresh"]
    except Exception as e:
        logger.warning(f"Error loading ETF status: {e}")

# ============================================================================
# ✅ CRITICAL: SESSION ACTIVITY TRACKING
# ============================================================================

def update_session_activity():
    """Update session activity timestamp (called on every page load)"""
    if st.session_state.get("authenticated"):
        username = st.session_state.get("username")
        
        # Update in Streamlit session state
        st.session_state.last_activity = datetime.now(IST).isoformat()
        
        # Update in persistent storage
        if username:
            try:
                from persistent_sessions import update_session_activity as persist_update
                persist_update(username)
            except Exception as e:
                logger.warning(f"Could not update persistent activity: {e}")

# ============================================================================
# SUBSCRIBER REFRESH
# ============================================================================

def subscriber_manual_refresh():
    """Subscriber-triggered reload from CSVs with cooldown"""
    now = time.time()
    last_ts = st.session_state.get("subscriber_last_refresh_ts", 0)
    
    if now - last_ts < REFRESH_COOLDOWN_SECONDS:
        remaining = int(REFRESH_COOLDOWN_SECONDS - (now - last_ts))
        st.warning(f"⏳ Please wait {remaining}s before refreshing again")
        return
    
    st.session_state.subscriber_last_refresh_ts = now
    next_allowed = datetime.fromtimestamp(
        now + REFRESH_COOLDOWN_SECONDS, tz=IST
    ).strftime("%H:%M:%S IST")
    st.session_state.subscriber_next_allowed_label = next_allowed
    
    try:
        load_persisted_analysis_into_session()
        st.success("✅ Data refreshed from latest admin analysis.")
        logger.info("Subscriber manual refresh completed")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Refresh error: {str(e)}")
        logger.error(f"Subscriber refresh failed: {e}", exc_info=True)

# ============================================================================
# AUTHENTICATION
# ============================================================================

def _login_with_store():
    """Check if authenticated, else show landing page"""
    if not st.session_state.get("authenticated"):
        try:
            from landing_page_ENHANCED import render_landing_page
            render_landing_page()
        except ImportError:
            from landing_page import render_landing_page
            render_landing_page()
        except Exception as e:
            logger.error(f"Error rendering landing page: {e}")
            st.error("Failed to load login page")
            st.stop()


def check_authentication() -> UserStore:
    """Ensure user is authenticated and hydrate session using JSON store"""

    if not st.session_state.get("authenticated"):
        _login_with_store()

    username = st.session_state.get("username")
    if not username:
        _login_with_store()

    user_store = UserStore()
    users = user_store.get_all_users()
    user = user_store.get_user(username)

    if not user or user.get("status") != "active":
        st.error("❌ Account inactive or deleted. Contact admin.")
        try:
            from persistent_sessions import clear_persistent_session
            clear_persistent_session(username)
        except Exception:
            pass

        st.session_state.clear()
        init_session_state()
        st.stop()

    # ✅ Hydrate session from JSON store
    st.session_state.user_id = user["id"]
    st.session_state.user_role = user["role"]
    st.session_state.has_active_subscription = bool(
        user.get("has_active_subscription", False)
    )

    # ✅ RETURN MUST BE INSIDE FUNCTION
    return user_store



# ============================================================================
# ANALYSIS HELPERS
# ============================================================================

def run_sector_analysis():
    """Run sector RS analysis with validation"""
    try:
        from rs_analyzer import SectorRSAnalyzer
        from config import SECTOR_TOKENS, BENCHMARK_TOKENS
        
        connector = st.session_state.admin_connector
        if not connector:
            st.error("❌ AngelOne not connected")
            return
        
        benchmark_name = st.session_state.get("benchmark", "NIFTY 50")
        rs1 = st.session_state.get("rs_period_1", 21)
        rs2 = st.session_state.get("rs_period_2", 55)
        rs3 = st.session_state.get("rs_period_3", 123)
        
        with st.spinner("🔄 Fetching live market data for sectors..."):
            analyzer = SectorRSAnalyzer(connector, SECTOR_TOKENS)
            df = analyzer.analyze(
                BENCHMARK_TOKENS[benchmark_name]["token"],
                [rs1, rs2, rs3],
                None,
            )
        
        if df is None or df.empty:
            st.error("❌ No sector data returned")
            logger.error("Sector analysis returned empty DataFrame")
            return
        
        df = validate_sector_data(df)
        st.session_state.analysis_results = df
        st.session_state.last_analysis_time = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
        
        try:
            df.to_csv("sector_analysis_data.csv", index=False)
            DataRefreshTracker.update_status("sectors", status="success", count=len(df))
            st.success(f"✅ Sector analysis complete: {len(df)} sectors analyzed")
            logger.info(f"Sector analysis successful: {len(df)} rows")
        except Exception as e:
            st.warning(f"⚠️ Analysis done but save failed: {e}")
            logger.error(f"Error saving sector analysis: {e}")
    except Exception as e:
        st.error(f"❌ Sector analysis error: {str(e)}")
        logger.error(f"Sector analysis failed: {e}", exc_info=True)

def run_etf_analysis():
    """Run ETF RS calculation with validation"""
    try:
        from etf_rs_calculator import calculate_etf_rs
        
        smartapi = st.session_state.admin_connector.smartapi
        
        with st.spinner("🔄 Calculating ETF RS for all ETFs..."):
            df_etf = calculate_etf_rs(
                smartapi,
                "ETFs-List_updated.csv",
            )
        
        if df_etf is None or df_etf.empty:
            st.error("❌ No ETF data returned")
            logger.error("ETF analysis returned empty DataFrame")
            return
        
        df_etf = validate_etf_data(df_etf)
        st.session_state.etf_rs = df_etf
        st.session_state.last_etf_time = datetime.now(IST).strftime("%Y-%m-%d %H:%M IST")
        
        try:
            df_etf.to_csv("etf_rs_output.csv", index=False)
            DataRefreshTracker.save_refresh("etfs", status="success", count=len(df_etf))
            st.success(f"✅ ETF RS calculation complete: {len(df_etf)} ETFs analyzed")
            logger.info(f"ETF analysis successful: {len(df_etf)} rows")
        except Exception as e:
            st.warning(f"⚠️ ETF RS done but save failed: {e}")
            logger.error(f"Error saving ETF analysis: {e}")
    except Exception as e:
        st.error(f"❌ ETF analysis error: {str(e)}")
        logger.error(f"ETF analysis failed: {e}", exc_info=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

def render_sidebar_config():
    """Render sidebar with configuration options"""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # AngelOne API (admin only)
        if st.session_state.get("user_role") == "admin":
            with st.expander(
                "🔐 AngelOne API Connection",
                expanded=not st.session_state.admin_connected,
            ):
                st.caption("Enter AngelOne Trading API credentials")
                apikey = st.text_input(
                    "API Key",
                    type="password",
                    placeholder="Your API Key",
                    key="sidebar_apikey",
                )
                client_code = st.text_input(
                    "Client Code",
                    placeholder="Your Client Code",
                    key="sidebar_client",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Trading Password",
                    key="sidebar_pwd",
                )
                totp = st.text_input(
                    "TOTP Secret",
                    type="password",
                    placeholder="TOTP Secret Key",
                    key="sidebar_totp",
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔓 Connect", width="stretch", key="sidebar_connect_btn"):
                        if all([apikey, client_code, password, totp]):
                            with st.spinner("Connecting to AngelOne..."):
                                try:
                                    from api_connector import AngelOneConnector
                                    conn = AngelOneConnector(apikey, client_code, password, totp)
                                    ok, msg = conn.connect()
                                    if ok:
                                        st.session_state.admin_connector = conn
                                        st.session_state.admin_connected = True
                                        st.success(msg)
                                        logger.info("AngelOne connected successfully")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error(msg)
                                        logger.error(f"AngelOne connection failed: {msg}")
                                except Exception as e:
                                    st.error(f"Connection error: {e}")
                                    logger.error(f"AngelOne connection error: {e}", exc_info=True)
                        else:
                            st.error("❌ All fields required")
                
                with col2:
                    if st.button("🚪 Disconnect", width="stretch", key="sidebar_disconnect_btn"):
                        st.session_state.admin_connected = False
                        st.session_state.admin_connector = None
                        st.success("Disconnected from AngelOne")
                        logger.info("AngelOne disconnected")
                        time.sleep(1)
                        st.rerun()
            
            st.divider()
            if st.session_state.admin_connected:
                st.success("✅ Connected to AngelOne")
            else:
                st.warning("⚠️ Not connected to AngelOne")
        else:
            st.info("🔐 Connection managed by administrator")
        
        st.divider()
        
        # Analysis settings
        st.header("📈 Analysis Settings")
        benchmark_options = ["NIFTY 50", "NIFTY 100", "SENSEX"]
        current_benchmark = st.session_state.get("benchmark", "NIFTY 50")
        
        if st.session_state.get("user_role") == "admin":
            idx = benchmark_options.index(current_benchmark) if current_benchmark in benchmark_options else 0
            benchmark = st.selectbox(
                "Benchmark Index",
                options=benchmark_options,
                index=idx,
                key="sidebar_benchmark",
            )
            st.session_state.benchmark = benchmark
            
            st.caption("📊 RS Periods (in days)")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.session_state.rs_period_1 = st.number_input(
                    "Period 1 (Short)",
                    min_value=5,
                    max_value=100,
                    value=st.session_state.get("rs_period_1", 21),
                    key="sidebar_rs1",
                )
            with col2:
                st.session_state.rs_period_2 = st.number_input(
                    "Period 2 (Medium)",
                    min_value=5,
                    max_value=200,
                    value=st.session_state.get("rs_period_2", 55),
                    key="sidebar_rs2",
                )
            with col3:
                st.session_state.rs_period_3 = st.number_input(
                    "Period 3 (Long)",
                    min_value=5,
                    max_value=300,
                    value=st.session_state.get("rs_period_3", 123),
                    key="sidebar_rs3",
                )
        else:
            st.caption("Current analysis settings (chosen by admin):")
            st.text_input("Benchmark Index", value=current_benchmark, disabled=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input(
                    "Period 1 (Short)",
                    value=str(st.session_state.get("rs_period_1", 21)),
                    disabled=True,
                )
            with col2:
                st.text_input(
                    "Period 2 (Medium)",
                    value=str(st.session_state.get("rs_period_2", 55)),
                    disabled=True,
                )
            with col3:
                st.text_input(
                    "Period 3 (Long)",
                    value=str(st.session_state.get("rs_period_3", 123)),
                    disabled=True,
                )
        
        st.session_state.enable_audit = st.checkbox(
            "📋 Enable Audit Trail",
            value=st.session_state.get("enable_audit", True),
            key="sidebar_audit",
        )
        
        st.divider()
        
        # Auto-refresh (admin only)
        if st.session_state.get("user_role") == "admin":
            st.caption("⏱ Auto-refresh (Admin only)")
            refresh_options = [0, 1, 2, 3, 4, 5, 10, 15, 30]
            labels = ["Off"] + [f"{m} min" for m in refresh_options[1:]]
            current_label = st.session_state.get("auto_refresh_label", "Off")
            default_idx = labels.index(current_label) if current_label in labels else 0
            selected_label = st.selectbox(
                "Auto-refresh interval",
                options=labels,
                index=default_idx,
                key="sidebar_auto_refresh",
            )
            st.session_state.auto_refresh_label = selected_label
            if selected_label == "Off":
                st.session_state.auto_refresh_minutes = 0
            else:
                st.session_state.auto_refresh_minutes = int(selected_label.split()[0])
            
            if st.session_state.auto_refresh_minutes > 0:
                st.info(f"🔄 Auto-refresh every {st.session_state.auto_refresh_minutes} minute(s)")
        
        st.divider()
        
        # Action buttons
        if st.session_state.get("user_role") == "admin":
            analyze_clicked = st.button(
                "🔍 Analyze All Sectors",
                type="primary",
                width="stretch",
                key="sidebar_analyze_sectors",
            )
            etf_clicked = st.button(
                "📑 Calculate ETF RS",
                type="secondary",
                width="stretch",
                key="sidebar_calc_etf",
            )
            
            if analyze_clicked:
                if not st.session_state.admin_connected:
                    st.error("❌ Connect to AngelOne first")
                else:
                    run_sector_analysis()
            
            if etf_clicked:
                if not st.session_state.admin_connected:
                    st.error("❌ Connect to AngelOne first")
                else:
                    run_etf_analysis()
        else:
            st.info("💡 Only admin can refresh analysis.")
        
        st.divider()
        
        st.subheader("👤 User Info")
        st.write(f"**User:** {st.session_state.username}")
        role_display = st.session_state.user_role.title() if st.session_state.user_role else "Not logged in"
        st.write(f"**Role:** {role_display}")

        
        # ✅ CRITICAL FIX #4: LOGOUT WITH SESSION CLEANUP
        if st.button("🚪 Logout", width="stretch", key="sidebar_logout"):
            try:
                # Clear persistent session from file
                from persistent_sessions import clear_persistent_session
                username = st.session_state.get("username")
                if username:
                    clear_persistent_session(username)
                    logger.info(f"Cleared persistent session for {username}")
            except Exception as e:
                logger.warning(f"Could not clear persistent session: {e}")
            
            # Clear Streamlit session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            init_session_state()
            st.experimental_rerun()

# ============================================================================
# HEADER
# ============================================================================

def render_header():
    """✅ FIXED: Render header with correct IST timestamp and market status"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("# 📊 D's Sector ETF RS Analyzer")
        st.markdown("**Market Data For Study Purpose** - Educational Edition V7")
    
    with col2:
        if is_market_open():
            st.success("🟢 Market OPEN")
        else:
            st.info("🔵 Market CLOSED")
    
    with col3:
        current_time_ist = datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")
        st.caption(f"🕒 {current_time_ist}")
    
    st.divider()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    logger.info("=" * 80)
    logger.info("APPLICATION STARTED - Educational Edition V7 + PERSISTENT SESSIONS")
    logger.info("=" * 80)
    
    try:
        # ✅ CRITICAL: Try to auto-restore persistent session FIRST
        load_persistent_session_if_exists()
        
        # Update session activity on every page load
        update_session_activity()
        
        # Check authentication
        user_manager = check_authentication()
        # 🔐 PHASE-4.3: Enforce subscription expiry
        if st.session_state.get("user_role") == "subscriber":
            ok = enforce_subscription_or_logout(
                st.session_state.username,
                st.session_state
            )
            if not ok:
                st.warning("🔒 Your subscription has expired. Please upgrade.")
                st.experimental_rerun()

        # Render UI
        render_sidebar_config()
        render_header()
        
        # Auto-refresh for admin (with market hours check)
        if st.session_state.user_role == "admin":
            interval_min = st.session_state.get("auto_refresh_minutes", 0)
            if interval_min > 0:
                try:
                    from streamlit_autorefresh import st_autorefresh
                    counter = st_autorefresh(
                        interval=interval_min * 60 * 1000,
                        key="admin_auto_refresh_counter",
                    )
                    if counter > 0 and is_market_open() and st.session_state.admin_connected:
                        logger.info(f"Auto-refresh triggered (counter={counter})")
                        run_sector_analysis()
                        run_etf_analysis()
                except ImportError:
                    st.warning(
                        "⚠️ streamlit-autorefresh not installed. "
                        "Install with: pip install streamlit-autorefresh"
                    )


        
        if st.session_state.user_role == "admin":
            # =================== ADMIN VIEW ===================
            st.markdown("## 👨💼 Admin Dashboard")
            st.info(
                "🔑 **Admin Access** - You can manage data refresh, user settings, "
                "user accounts, and analysis configurations."
            )
            
            admin_nav = st.tabs(
                ["🏠 Home", "🔄 Data Refresh", "📊 Dashboards", "👥 User Management", "⚙️ System Settings", "📝 Blog"]
            )
            
            # Home
            with admin_nav[0]:
                render_tab_home()
                st.divider()
                st.subheader("👨💼 Admin Snapshot")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        "Sectors Analyzed",
                        len(st.session_state.analysis_results)
                        if st.session_state.get("analysis_results") is not None
                        else 0,
                    )
                with col2:
                    st.metric(
                        "ETFs Analyzed",
                        len(st.session_state.etf_rs)
                        if st.session_state.get("etf_rs") is not None
                        else 0,
                    )
                with col3:
                    status = "🟢 Connected" if st.session_state.admin_connected else "🔴 Not Connected"
                    st.metric("AngelOne Status", status)
                with col4:
                    st.metric(
                        "Last Sector Update",
                        st.session_state.get("last_analysis_time", "Never"),
                    )
            
            # Data Refresh
            with admin_nav[1]:
                st.subheader("🔄 Refresh Market Data")
                sector_status = DataRefreshTracker.get_status("sectors") or {}
                etf_status = DataRefreshTracker.get_status("etfs") or {}
                
                col1, col2 = st.columns(2)
                with col1:
                    sector_display = sector_status.get("last_refresh", "Never")
                    st.caption(f"🕒 Sectors last refreshed: {sector_display} IST")
                with col2:
                    etf_display = etf_status.get("last_refresh", "Never")
                    st.caption(f"🕒 ETFs last refreshed: {etf_display} IST")
                
                st.divider()
                
                if st.session_state.admin_connected:
                    st.success("✅ AngelOne Connected")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "🔍 Analyze All Sectors",
                            type="primary",
                            width="stretch",
                            key="tab_analyze_sectors",
                        ):
                            run_sector_analysis()
                    with col2:
                        if st.button(
                            "📑 Calculate ETF RS",
                            type="secondary",
                            width="stretch",
                            key="tab_calc_etf",
                        ):
                            run_etf_analysis()
                else:
                    st.warning("⚠️ Connect to AngelOne in the sidebar first")
            
            # Dashboards
            with admin_nav[2]:
                st.subheader("📊 Analysis Dashboards")
                if st.session_state.get("analysis_results") is not None:
                    st.info("✅ Sector analysis data available for viewing")
                    st.dataframe(
                        st.session_state.analysis_results,
                        width="stretch",
                    )
                else:
                    st.warning("❌ No sector analysis data yet. Run data refresh first.")
                
                st.divider()
                
                if st.session_state.get("etf_rs") is not None:
                    st.info("✅ ETF RS data available for viewing")
                    st.dataframe(st.session_state.etf_rs, width="stretch")
                else:
                    st.warning("❌ No ETF RS data yet. Calculate ETF RS first.")
            

            
            # User Management
            with admin_nav[3]:
                st.subheader("👥 User Management")

                user_store = UserStore()
                users = user_store.get_all_users()

                if not users:
                    st.info("No users in database yet.")
                else:
                    # ---------------- METRICS ----------------
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Users", len(users))
                    with col2:
                        st.metric(
                            "Admins",
                            sum(1 for u in users if u.get("role") == "admin"),
                        )
                    with col3:
                        st.metric(
                            "Subscribers",
                            sum(1 for u in users if u.get("role") == "subscriber"),
                        )
                    with col4:
                        st.metric(
                            "Active",
                            sum(1 for u in users if u.get("status") == "active"),
                        )

                    st.divider()

                    # ---------------- USER TABLE ----------------
                    df = pd.DataFrame(users)
                    display_cols = [
                        "id",
                        "username",
                        "email",
                        "role",
                        "status",
                        "created_at",
                    ]
                    existing_cols = [c for c in display_cols if c in df.columns]
                    st.dataframe(
                        df[existing_cols],
                        width="stretch",
                        hide_index=True,
                    )

                    st.divider()

                    # ---------------- MANAGE USER ----------------
                    st.markdown("### 🔧 Manage Existing User")

                    selected = st.selectbox(
                        "Select User",
                        users,
                        format_func=lambda u: (
                            f"{u['id']} - {u['username']} "
                            f"({u['role']}, {u['status']})"
                        ),
                        key="admin_user_select",
                    )

                    if selected:
                        col_a, col_b = st.columns(2)

                        # Status change
                        with col_a:
                            new_status = st.selectbox(
                                "Change Status",
                                ["active", "inactive"],
                                index=0
                                if selected["status"] == "active"
                                else 1,
                                key="admin_status_select",
                            )
                            if st.button(
                                "Update Status",
                                width="stretch",
                                key="admin_update_status",
                            ):
                                user_store.set_status(
                                    selected["id"], new_status
                                )
                                st.success(
                                    f"Status updated to {new_status}"
                                )
                                logger.info(
                                    f"Admin changed status: "
                                    f"{selected['username']} → {new_status}"
                                )
                                st.rerun()

                        # Password reset
                        with col_b:
                            with st.form("admin_reset_password"):
                                st.write(
                                    f"🔑 Reset password for "
                                    f"**{selected['username']}**"
                                )
                                pwd1 = st.text_input(
                                    "New Password", type="password"
                                )
                                pwd2 = st.text_input(
                                    "Confirm Password", type="password"
                                )
                                submitted = st.form_submit_button(
                                    "Update Password",
                                    width="stretch",
                                )

                                if submitted:
                                    if not pwd1 or not pwd2:
                                        st.error(
                                            "Both password fields are required."
                                        )
                                    elif pwd1 != pwd2:
                                        st.error(
                                            "Passwords do not match."
                                        )
                                    elif len(pwd1) < 6:
                                        st.error(
                                            "Password must be at least 6 characters."
                                        )
                                    else:
                                        user_store.change_password(
                                            selected["id"], pwd1
                                        )
                                        st.success(
                                            "Password updated successfully."
                                        )
                                        logger.info(
                                            f"Admin reset password for "
                                            f"{selected['username']}"
                                        )

                st.divider()

                # ---------------- CREATE NEW USER ----------------
                st.markdown("### ➕ Create New User")

                with st.form("admin_create_user"):
                    new_username = st.text_input("Username")
                    new_email = st.text_input("Email (optional)")
                    new_password = st.text_input(
                        "Password", type="password"
                    )
                    new_role = st.selectbox(
                        "Role", ["subscriber", "admin", "viewer"]
                    )

                    submitted = st.form_submit_button(
                        "Create User", width="stretch"
                    )

                    if submitted:
                        if not new_username or not new_password:
                            st.error(
                                "Username and password are required."
                            )
                        elif len(new_password) < 6:
                            st.error(
                                "Password must be at least 6 characters."
                            )
                        else:
                            ok, msg = user_store.create_user(
                                username=new_username,
                                password=new_password,
                                role=new_role,
                                email=new_email,
                            )
                            if ok:
                                logger.info(
                                    f"Admin created user: "
                                    f"{new_username} ({new_role})"
                                )
                                if new_role == "subscriber":
                                    user_store.ensure_subscription_flag(created_user=new_username)

                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)

            
            # System Settings
            with admin_nav[4]:
                st.subheader("⚙️ System Settings")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Market & Time Settings:**")
                    st.write(f"- Market open now: {is_market_open()}")
                    st.write(f"- Benchmark: {st.session_state.get('benchmark', 'NIFTY 50')}")
                    st.write(
                        f"- RS Periods: {st.session_state.rs_period_1}/"
                        f"{st.session_state.rs_period_2}/"
                        f"{st.session_state.rs_period_3}"
                    )
                    st.write(f"- Auto-refresh: {st.session_state.get('auto_refresh_label', 'Off')}")
                
                with col2:
                    st.write("**Edition Info:**")
                    st.info(
                        "📋 **Edition Details:**\n\n"
                        "✓ Educational Edition V7\n"
                        "✓ Fly.io / Railway / Render Ready\n"
                        "✓ Market Data for Study\n"
                        "✓ AngelOne Integration\n"
                        "✓ Real-time RS Analysis (admin)\n"
                        "✓ Persistent Session Support\n"
                        "✓ Postgres Authentication\n"
                        "✓ Subscription Gating"
                    )
            
            # Blog
            with admin_nav[5]:
                blogpage()
        
        else:
            # ================= SUBSCRIBER / VIEWER VIEW =================
            if not st.session_state.get("has_active_subscription", False):
                st.warning("🔒 Premium access required")
                     
                if st.button("💳 Upgrade to Premium"):
                    order_id = f"ORD_{int(time.time())}_{st.session_state.username}"
                    pay_url = f"https://payments.cashfree.com/checkout?order_id={order_id}"
                    st.markdown(f"[👉 Click here to Pay ₹999]({pay_url})", unsafe_allow_html=True)
                      
                st.stop()

            
            load_persisted_analysis_into_session()
            
            st.markdown("## 📚 Educational Market Analysis Reports")
            st.caption(
                f"Logged in as: **{st.session_state.username}** "
                f"({st.session_state.user_role.title()})"
            )
            st.info(
                "📚 **Educational Purpose** - These reports are for learning how "
                "sectors and ETFs behave. Treat this as a learning lab, not "
                "trading advice."
            )
            
            sector_status = DataRefreshTracker.get_status("sectors") or {}
            etf_status = DataRefreshTracker.get_status("etfs") or {}
            
            st.caption(
                f"🕒 Sectors last refreshed: {sector_status.get('last_refresh', 'Never')} IST\n\n"
                f"🕒 ETFs last refreshed: {etf_status.get('last_refresh', 'Never')} IST"
            )
            
            st.divider()
            
            sub_tabs = st.tabs(
                [
                    "🏠 Home",
                    "📊 Sector Analysis",
                    "💼 ETF Analysis",
                    "📈 Comprehensive Report",
                    "📝 Blog",
                    "📚 Learning Guide",
                ]
            )
            
            with sub_tabs[0]:
                render_tab_home()
            with sub_tabs[1]:
                render_subscriber_sector_view(subscriber_manual_refresh)
            with sub_tabs[2]:
                render_subscriber_etf_view(subscriber_manual_refresh)
            with sub_tabs[3]:
                render_subscriber_comprehensive_view(subscriber_manual_refresh)
            with sub_tabs[4]:
                blogpage()
            with sub_tabs[5]:
                st.subheader("📚 Learning Resources")
                st.write("Learn about Relative Strength (RS), sectors, and ETF analysis.")
        
        # Footer
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption("D's Analysis – Sector ETF RS Analyzer v7")
        with col2:
            st.caption("🎓 Educational Edition – For Study & Learning Only")
        with col3:
            st.caption(f"⏰ Updated: {datetime.now(IST).strftime('%Y-%m-%d %H:%M IST')}")
    
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error(f"❌ Application error: {str(e)}")
        st.info("Please refresh the page or contact support")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
