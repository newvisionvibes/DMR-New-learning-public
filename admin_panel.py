"""
ADMIN CONTROL PANEL – PRODUCTION READY (FINAL)

Features (FULLY INTEGRATED):
✔ Manual refresh: Sector / ETF / Both
✔ Automatic hourly refresh during market hours
✔ Market hours aware (9:15–15:30 IST, Mon–Fri)
✔ AngelOne secure connection
✔ Persistent timestamps via DataRefreshTracker
✔ Subscriber + Admin views always consistent
✔ Fly.io safe (no background threads)
"""

import streamlit as st
from datetime import datetime, time as dt_time
import pytz
import pandas as pd

from data_refresh_tracker import DataRefreshTracker
from api_connector import AngelOneConnector
from rs_analyzer import SectorRSAnalyzer
from etf_rs_calculator import calculate_etf_rs
from config import SECTOR_TOKENS, BENCHMARK_TOKENS

# =============================================================================
# TIMEZONE & MARKET HOURS
# =============================================================================

IST = pytz.timezone("Asia/Kolkata")

def is_market_hours(now=None):
    if now is None:
        now = datetime.now(IST)

    market_start = dt_time(9, 15)
    market_end = dt_time(15, 30)

    return (
        now.weekday() < 5 and
        market_start <= now.time() <= market_end
    )

# =============================================================================
# CORE REFRESH ENGINE (SINGLE SOURCE)
# =============================================================================

def refresh_all_data(connector, run_sector=True, run_etf=True, is_auto=False):
    now = datetime.now(IST)

    # ---------------- Sector Analysis ----------------
    if run_sector:
        analyzer = SectorRSAnalyzer(connector, SECTOR_TOKENS)
        df_sector = analyzer.analyze(
            BENCHMARK_TOKENS["NIFTY 50"]["token"],
            [21, 55, 123],
            None
        )

        if df_sector is None or df_sector.empty:
            return False, "Sector analysis returned no data"

        st.session_state.analysis_results = df_sector
        DataRefreshTracker.save_refresh("sectors")

    # ---------------- ETF Analysis ----------------
    if run_etf:
        df_etf = calculate_etf_rs(connector.smartapi, "ETFs-List_updated.csv")
        if df_etf is not None and not df_etf.empty:
            st.session_state.etf_rs = df_etf
            DataRefreshTracker.save_refresh("etfs")

    # ---------------- Comprehensive ----------------
    if run_sector and run_etf:
        DataRefreshTracker.save_refresh("comprehensive")

    st.session_state.last_auto_refresh_time = now

    mode = "Auto" if is_auto else "Manual"
    return True, f"{mode} refresh completed at {now.strftime('%H:%M:%S IST')}"

# =============================================================================
# MAIN ADMIN PANEL
# =============================================================================

def render_admin_panel(user_manager):

    if st.session_state.user_role != "admin":
        st.error("Admin access required")
        return

    st.subheader("👨‍💼 Admin Control Panel")
    st.divider()

    # -------------------------------------------------------------------------
    # ADMIN TABS
    # -------------------------------------------------------------------------
    tab_users, tab_refresh, tab_status, tab_security = st.tabs([
        "👥 User Management",
        "🔄 Data Refresh",
        "📊 System Status",
        "🔐 Security",
    ])

    # =========================================================================
    # TAB 1 — USER MANAGEMENT (UNCHANGED, SAFE)
    # =========================================================================
    with tab_users:
        users = user_manager.get_all_users()
        st.metric("Total Users", len(users))
        st.dataframe(
            pd.DataFrame.from_dict(users, orient="index"),
            width="stretch"
        )

    # =========================================================================
    # TAB 2 — DATA REFRESH (FIXED + UNIFIED)
    # =========================================================================
    with tab_refresh:
        now = datetime.now(IST)
        market_open = is_market_hours(now)

        if market_open:
            st.success("📈 Market OPEN")
        else:
            st.warning("📉 Market CLOSED")

        st.caption("Auto-refresh runs hourly during market hours")

        # ---------------- AngelOne Connection ----------------
        with st.expander("🔐 AngelOne API Connection", expanded=False):
            apikey = st.text_input("API Key", type="password")
            client = st.text_input("Client Code")
            pwd = st.text_input("Password", type="password")
            totp = st.text_input("TOTP Secret", type="password")

            if st.button("🔓 Connect"):
                if all([apikey, client, pwd, totp]):
                    conn = AngelOneConnector(apikey, client, pwd, totp)
                    ok, msg = conn.connect()
                    if ok:
                        st.session_state.admin_connector = conn
                        st.session_state.admin_connected = True
                        st.success("Connected to AngelOne")
                    else:
                        st.error(msg)
                else:
                    st.error("All fields required")

        if not st.session_state.get("admin_connected"):
            st.warning("AngelOne not connected")
            return

        # ---------------- AUTO REFRESH ----------------
        last_auto = st.session_state.get("last_auto_refresh_time")
        if market_open:
            if last_auto is None or (now - last_auto).total_seconds() > 3600:
                with st.spinner("🤖 Auto-refreshing..."):
                    ok, msg = refresh_all_data(
                        st.session_state.admin_connector,
                        run_sector=True,
                        run_etf=True,
                        is_auto=True
                    )
                    if ok:
                        st.success(msg)

        # ---------------- MANUAL BUTTONS ----------------
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Analyze Sectors"):
                ok, msg = refresh_all_data(
                    st.session_state.admin_connector,
                    run_sector=True,
                    run_etf=False
                )
                st.success(msg)

        with col2:
            if st.button("💼 Analyze ETF"):
                ok, msg = refresh_all_data(
                    st.session_state.admin_connector,
                    run_sector=False,
                    run_etf=True
                )
                st.success(msg)

        with col3:
            if st.button("🔄 Analyze Both"):
                ok, msg = refresh_all_data(
                    st.session_state.admin_connector,
                    run_sector=True,
                    run_etf=True
                )
                st.success(msg)

    # =========================================================================
    # TAB 3 — SYSTEM STATUS (ALIGNED WITH TRACKER)
    # =========================================================================
    with tab_status:
        col1, col2, col3 = st.columns(3)

        s = DataRefreshTracker.get_status("sectors")
        e = DataRefreshTracker.get_status("etfs")
        c = DataRefreshTracker.get_status("comprehensive")

        col1.metric("Sector Data", s["freshness"].capitalize(), s["last_refresh"])
        col2.metric("ETF Data", e["freshness"].capitalize(), e["last_refresh"])
        col3.metric("Combined", c["freshness"].capitalize(), c["last_refresh"])

    # =========================================================================
    # TAB 4 — SECURITY (UNCHANGED)
    # =========================================================================
    with tab_security:
        st.info(
            "✔ Change admin password regularly\n"
            "✔ Do not share AngelOne credentials\n"
            "✔ Auto-refresh only during market hours"
        )
