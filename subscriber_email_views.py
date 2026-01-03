"""
SUBSCRIBER EMAIL VIEWS - WITH MANUAL, RATE-LIMITED REFRESH

Subscribers see email-style reports and can refresh data manually.
The refresh button is disabled during cooldown and shows the next
allowed refresh time as a clock value (HH:MM:SS IST).
"""

import time
import streamlit as st

from data_refresh_tracker import DataRefreshTracker
from sector_rs_email_builder_v541 import (
    generate_sector_newsletter_v541,
    generate_etf_newsletter_v541,
    generate_comprehensive_newsletter_v541,
)

# Must match main.py
REFRESH_COOLDOWN_SECONDS = 60


# ============================================================================
# SHARED HELPERS
# ============================================================================

def render_data_refresh_info(analysis_type: str):
    """Display last data refresh timestamp for subscribers (read-only)."""
    status = DataRefreshTracker.get_status(analysis_type) or {}

    last_refresh = status.get("last_refresh")
    freshness = status.get("freshness")

    # Build optional freshness suffix safely
    if isinstance(freshness, str) and freshness.strip():
        freshness_text = f" ({freshness.capitalize()})"
    else:
        freshness_text = ""

    if last_refresh and last_refresh != "Never":
        st.caption(
            f"🕒 **Data last refreshed:** {last_refresh} IST{freshness_text}"
        )
    else:
        st.caption("🕒 **Data refresh information not available yet**")


def _render_refresh_ui(button_key: str, on_refresh):
    """
    Shared refresh UI with cooldown and next-allowed time label.

    on_refresh is subscriber_manual_refresh from main.py.
    """
    now_ts = time.time()
    last_ts = st.session_state.get("subscriber_last_refresh_ts", 0)
    label = st.session_state.get("subscriber_next_allowed_label")

    # Derive exact 'next allowed' timestamp from last_ts
    next_allowed_ts = last_ts + REFRESH_COOLDOWN_SECONDS if last_ts > 0 else 0
    in_cooldown = next_allowed_ts > 0 and now_ts < next_allowed_ts

    if in_cooldown:
        # Draw a clickable button but ignore clicks during real cooldown
        clicked = st.button("🔄 Refresh data", key=button_key)
        if label:
            st.info(f"⏳ Next refresh allowed after **{label}**.")
        else:
            st.info("⏳ Next refresh allowed after the cooldown window.")

        # If user clicks *after* cooldown has actually passed, force rerun
        if clicked and not (time.time() < next_allowed_ts):
            st.session_state.subscriber_next_allowed_label = None
            st.rerun()
    else:
        # Cooldown over → clear label and allow real refresh
        st.session_state.subscriber_next_allowed_label = None
        if st.button("🔄 Refresh data", key=button_key):
            on_refresh()


# ============================================================================
# SECTOR ANALYSIS (SUBSCRIBER VIEW)
# ============================================================================

def render_subscriber_sector_view(on_refresh):
    """
    Display Sector Analysis in email format for subscribers.
    Includes a manual, rate-limited refresh button.
    """
    st.subheader("📊 Sector Analysis Report")

    cols = st.columns([3, 1])
    with cols[0]:
        render_data_refresh_info("sectors")
    with cols[1]:
        _render_refresh_ui("sub_refresh_sectors", on_refresh)

    if st.session_state.get("analysis_results") is None:
        st.warning("📊 No sector data available. Please check back later.")
        return

    df = st.session_state.analysis_results
    benchmark = st.session_state.get("benchmark", "NIFTY 50")

    st.divider()

    email_html = generate_sector_newsletter_v541(df, benchmark)
    st.components.v1.html(email_html, height=2000, scrolling=True)


# ============================================================================
# ETF ANALYSIS (SUBSCRIBER VIEW)
# ============================================================================

def render_subscriber_etf_view(on_refresh):
    """
    Display ETF Analysis in email format for subscribers.
    Includes a manual, rate-limited refresh button.
    """
    st.subheader("💼 ETF Analysis Report")

    cols = st.columns([3, 1])
    with cols[0]:
        render_data_refresh_info("etfs")
    with cols[1]:
        _render_refresh_ui("sub_refresh_etfs", on_refresh)

    if st.session_state.get("etf_rs") is None:
        st.warning("💼 No ETF data available. Please check back later.")
        return

    etf_df = st.session_state.etf_rs

    st.divider()

    email_html = generate_etf_newsletter_v541(etf_df)
    st.components.v1.html(email_html, height=2000, scrolling=True)


# ============================================================================
# COMPREHENSIVE ANALYSIS (SUBSCRIBER VIEW)
# ============================================================================

def render_subscriber_comprehensive_view(on_refresh):
    """
    Display Comprehensive Analysis for subscribers.
    Includes a manual, rate-limited refresh button.
    Shows both Sector and ETF reports combined.
    """
    st.subheader("📈 Comprehensive Market Analysis Report")

    cols = st.columns([3, 1])
    with cols[0]:
        render_data_refresh_info("comprehensive")
    with cols[1]:
        _render_refresh_ui("sub_refresh_comp", on_refresh)

    if (
        st.session_state.get("analysis_results") is None
        or st.session_state.get("etf_rs") is None
    ):
        st.warning("📈 Comprehensive analysis requires both sector and ETF data.")
        return

    sector_df = st.session_state.analysis_results
    etf_df = st.session_state.etf_rs
    benchmark = st.session_state.get("benchmark", "NIFTY 50")

    st.divider()

    email_html = generate_comprehensive_newsletter_v541(
        sector_df, etf_df, benchmark
    )
    st.components.v1.html(email_html, height=2500, scrolling=True)
