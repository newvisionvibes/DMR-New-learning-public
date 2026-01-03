"""
EMAIL DISTRIBUTION TAB - PRODUCTION FIXED VERSION
Handles SMTP testing and sending Sector / ETF / Comprehensive newsletters

FIXES:
✅ Removed invalid width="stretch" from all buttons
✅ Uses width="stretch" (Streamlit compatible)
✅ No logic changes
"""

import streamlit as st
from datetime import datetime

from email_sender import EmailSender
from sector_rs_email_builder_v541 import (
    generate_sector_newsletter_v541,
    generate_etf_newsletter_v541,
    generate_comprehensive_newsletter_v541,
)
from data_refresh_tracker import DataRefreshTracker


# ============================================================================
# MAIN RENDER FUNCTION
# ============================================================================

def render_tab_email(user_manager):

    st.subheader("📧 Email Distribution")

    # ---------------------------------------------------------------------
    # SMTP CONFIGURATION
    # ---------------------------------------------------------------------
    st.markdown("### 🔧 SMTP Configuration")

    col1, col2 = st.columns(2)
    with col1:
        smtp_server = st.text_input("SMTP Server", value="smtp.gmail.com")
        smtp_port = st.number_input("SMTP Port", value=587, step=1)
    with col2:
        sender_email = st.text_input("Sender Email")
        app_password = st.text_input(
            "App Password",
            type="password",
            help="Use Gmail App Password or SMTP password",
        )

    sender = EmailSender(
        smtp_server,
        smtp_port,
        sender_email,
        app_password,
    )

    if st.button("🔗 Test Connection", width="stretch"):
        ok, msg = sender.test_connection()
        if ok:
            st.success("✅ Email configuration verified and ready to send!")
        else:
            st.error(msg)

    st.divider()

    # ---------------------------------------------------------------------
    # RECIPIENT SETTINGS
    # ---------------------------------------------------------------------
    st.markdown("### 🧾 Newsletter Recipients")

    recipient_email = st.text_input(
        "Recipient Email Address",
        placeholder="user@example.com",
    )

    custom_note = st.text_area(
        "Custom Note (Optional)",
        placeholder="Optional message to include in the email...",
        height=80,
    )

    st.divider()

    # ---------------------------------------------------------------------
    # SEND SECTOR NEWSLETTER
    # ---------------------------------------------------------------------
    st.markdown("### 📊 Send Newsletter")

    if st.button(
        "📊 Send Sector Newsletter",
        width="stretch",
        key="send_sector_newsletter",
    ):
        if st.session_state.get("analysis_results") is None:
            st.warning("No sector data available.")
        else:
            html = generate_sector_newsletter_v541(
                st.session_state.analysis_results,
                st.session_state.get("benchmark", "NIFTY 50"),
            )
            ok, msg = sender.send_email(
                recipient_email,
                "📊 Sector RS Analysis (Educational)",
                html + (f"<hr><p>{custom_note}</p>" if custom_note else ""),
            )
            st.success(msg) if ok else st.error(msg)

    # ---------------------------------------------------------------------
    # SEND ETF NEWSLETTER
    # ---------------------------------------------------------------------
    if st.button(
        "💼 Send ETF Newsletter",
        width="stretch",
        key="send_etf_newsletter",
    ):
        if st.session_state.get("etf_rs") is None:
            st.warning("No ETF data available.")
        else:
            html = generate_etf_newsletter_v541(st.session_state.etf_rs)
            ok, msg = sender.send_email(
                recipient_email,
                "💼 ETF RS Analysis (Educational)",
                html + (f"<hr><p>{custom_note}</p>" if custom_note else ""),
            )
            st.success(msg) if ok else st.error(msg)

    # ---------------------------------------------------------------------
    # SEND COMPREHENSIVE NEWSLETTER
    # ---------------------------------------------------------------------
    if st.button(
        "📈 Send Comprehensive Newsletter",
        width="stretch",
        key="send_comp_newsletter",
    ):
        if (
            st.session_state.get("analysis_results") is None
            or st.session_state.get("etf_rs") is None
        ):
            st.warning("Sector + ETF data required.")
        else:
            html = generate_comprehensive_newsletter_v541(
                st.session_state.analysis_results,
                st.session_state.etf_rs,
                st.session_state.get("benchmark", "NIFTY 50"),
            )
            ok, msg = sender.send_email(
                recipient_email,
                "📈 Comprehensive Market Analysis (Educational)",
                html + (f"<hr><p>{custom_note}</p>" if custom_note else ""),
            )
            st.success(msg) if ok else st.error(msg)

    st.divider()

    # ---------------------------------------------------------------------
    # LAST SENT INFO (ADMIN VISIBILITY)
    # ---------------------------------------------------------------------
    status = DataRefreshTracker.get_status("etfs")
    st.caption(
        f"🕒 Data last updated: {status.get('last_refresh', 'Unknown')} "
        f"({status.get('freshness', 'unknown').capitalize()})"
    )
