"""
Output Renderers Module - PRODUCTION FIXED VERSION (ENHANCED)
Shared rendering functions for Sector, ETF, and Comprehensive views
Used by both admin preview tabs and subscriber dashboards

FIXES:
✅ Email Preview now uses st.expander() (reliable, no rerun issues)
✅ Removed fragile session_state preview flags
✅ Fully Fly.io compatible
"""

import streamlit as st
import pandas as pd
from datetime import datetime

from ui_components import (
    get_color_for_rs,
    get_color_for_pct_change,
    classify_etf_strategy
)

from sector_rs_email_builder_v541 import (
    generate_sector_newsletter_v541,
    generate_etf_newsletter_v541,
    generate_comprehensive_newsletter_v541
)

from data_refresh_tracker import render_refresh_header


# ============================================================================
# UNIQUE KEY GENERATOR
# ============================================================================

def get_unique_key(prefix: str) -> str:
    if "button_counter" not in st.session_state:
        st.session_state.button_counter = 0
    st.session_state.button_counter += 1
    return f"{prefix}_{st.session_state.button_counter}"


# ============================================================================
# SECTOR OUTPUT VIEW
# ============================================================================

def render_sector_output_view(show_admin_controls: bool = False):

    render_refresh_header("sectors", "📊", "Sector Analysis")

    if st.session_state.get("analysis_results") is None:
        st.warning("📊 No sector data available. Admin needs to run analysis.")
        return

    df = st.session_state.analysis_results

    rs_cols = [c for c in df.columns if c.startswith("RS_")]
    rs1, rs2, rs3 = (
        rs_cols[0] if len(rs_cols) > 0 else "RS_21",
        rs_cols[1] if len(rs_cols) > 1 else "RS_55",
        rs_cols[2] if len(rs_cols) > 2 else "RS_123",
    )

    # ── Summary
    st.subheader("📊 Sector Summary")
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🟢 Outperforming", len(df[df["Category"] == "Outperforming"]))
    c2.metric("🟡 Mixed", len(df[df["Category"] == "Mixed"]))
    c3.metric("🔴 Underperforming", len(df[df["Category"] == "Underperforming"]))

    last_time = st.session_state.get("last_analysis_time")
    c4.metric("⏰ Last Updated", last_time.strftime("%I:%M %p IST") if last_time else "--")

    st.divider()

    # ── Complete Table
    st.subheader("📊 Complete Sector Data Table")

    try:
        styled = df.style.format({
            "LTP": "{:.2f}",
            "Change": "{:.2f}",
            rs1: "{:.2f}",
            rs2: "{:.2f}",
            rs3: "{:.2f}",
        })

        try:
            styled = styled.map(get_color_for_rs, subset=[rs1, rs2, rs3]) \
                           .map(get_color_for_pct_change, subset=["Change"])
        except AttributeError:
            styled = styled.applymap(get_color_for_rs, subset=[rs1, rs2, rs3]) \
                           .applymap(get_color_for_pct_change, subset=["Change"])

        st.dataframe(styled, width="stretch", height=500)

    except Exception:
        st.dataframe(df, width="stretch", height=500)

    st.divider()

    # ── Admin Export
    if show_admin_controls:
        st.subheader("⬇️ Admin Export Options")
        c1, c2 = st.columns(2)

        c1.download_button(
            "📥 Download CSV",
            df.to_csv(index=False),
            f"sector_rs_{datetime.now():%Y%m%d_%H%M%S}.csv",
            "text/csv",
            width="stretch",
            key=get_unique_key("sector_csv"),
        )

        c2.download_button(
            "📧 Download Email HTML",
            generate_sector_newsletter_v541(df, st.session_state.get("benchmark", "NIFTY 50")),
            f"sector_email_{datetime.now():%Y%m%d_%H%M%S}.html",
            "text/html",
            width="stretch",
            key=get_unique_key("sector_html"),
        )

        with st.expander("👁️ Preview Email"):
            st.components.v1.html(
                generate_sector_newsletter_v541(df, st.session_state.get("benchmark", "NIFTY 50")),
                height=1000,
                scrolling=True,
            )


# ============================================================================
# ETF OUTPUT VIEW
# ============================================================================

def render_etf_output_view(show_admin_controls: bool = False):

    render_refresh_header("etfs", "💼", "ETF Analysis")

    if st.session_state.get("etf_rs") is None:
        st.warning("💼 No ETF data available. Admin needs to calculate ETF RS.")
        return

    etf_df = st.session_state.etf_rs.copy()
    etf_df["Strategy"] = etf_df.apply(classify_etf_strategy, axis=1)

    st.subheader("📊 Complete ETF Data Table")

    try:
        styled = etf_df.style.format({
            "LTP": "{:.2f}",
            "% Change": "{:.2f}",
            "RS_21": "{:.2f}",
            "RS_55": "{:.2f}",
            "RS_123": "{:.2f}",
        })

        try:
            styled = styled.map(get_color_for_pct_change, subset=["% Change"]) \
                           .map(get_color_for_rs, subset=["RS_21", "RS_55", "RS_123"])
        except AttributeError:
            styled = styled.applymap(get_color_for_pct_change, subset=["% Change"]) \
                           .applymap(get_color_for_rs, subset=["RS_21", "RS_55", "RS_123"])

        st.dataframe(styled, width="stretch", height=500)

    except Exception:
        st.dataframe(etf_df, width="stretch", height=500)

    st.divider()

    if show_admin_controls:
        st.subheader("⬇️ Admin Export Options")
        c1, c2 = st.columns(2)

        c1.download_button(
            "📥 Download CSV",
            etf_df.to_csv(index=False),
            f"etf_rs_{datetime.now():%Y%m%d_%H%M%S}.csv",
            "text/csv",
            width="stretch",
            key=get_unique_key("etf_csv"),
        )

        c2.download_button(
            "📧 Download Email HTML",
            generate_etf_newsletter_v541(etf_df),
            f"etf_email_{datetime.now():%Y%m%d_%H%M%S}.html",
            "text/html",
            width="stretch",
            key=get_unique_key("etf_html"),
        )

        with st.expander("👁️ Preview Email"):
            st.components.v1.html(
                generate_etf_newsletter_v541(etf_df),
                height=1000,
                scrolling=True,
            )


# ============================================================================
# COMPREHENSIVE OUTPUT VIEW
# ============================================================================

def render_comprehensive_output_view(show_admin_controls: bool = False):

    render_refresh_header("comprehensive", "📈", "Comprehensive Market Analysis")

    if st.session_state.get("analysis_results") is None or st.session_state.get("etf_rs") is None:
        st.warning("📈 Comprehensive analysis requires both sector and ETF data.")
        return

    sector_df = st.session_state.analysis_results
    etf_df = st.session_state.etf_rs.copy()
    etf_df["Strategy"] = etf_df.apply(classify_etf_strategy, axis=1)

    if show_admin_controls:
        with st.expander("👁️ Preview Email"):
            st.components.v1.html(
                generate_comprehensive_newsletter_v541(
                    sector_df,
                    etf_df,
                    st.session_state.get("benchmark", "NIFTY 50"),
                ),
                height=1200,
                scrolling=True,
            )
