"""
Enhanced Sectors Tab Renderer - With Sidebar AngelOne & Analysis Settings
Fly.io Deployment Ready - V7
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")


def render_tab_sectors():
    """Render sectors analysis tab with sidebar configuration"""

    # ===================================================================== #
    # SIDEBAR CONFIGURATION
    # ===================================================================== #
    with st.sidebar:
        st.header("⚙️ Configuration")

        # AngelOne API (status only here, connection handled in main sidebar)
        if st.session_state.get("user_role") == "admin":
            with st.expander(
                "🔐 AngelOne API", expanded=not st.session_state.admin_connected
            ):
                st.caption("Connection status")

                if st.session_state.admin_connected:
                    st.success("✅ Connected to AngelOne")
                else:
                    st.warning("⚠️ Not connected")
                    st.caption("Use main sidebar to connect")
        else:
            st.info("🔐 Connection managed by administrator")

        st.divider()

        # Analysis Settings
        st.header("📈 Sector Analysis Settings")

        benchmark = st.selectbox(
            "Benchmark Index",
            options=["NIFTY 50", "NIFTY 100", "SENSEX"],
            index=0 if st.session_state.get("benchmark", "NIFTY 50") == "NIFTY 50" else 1,
            key="sector_benchmark",
            help="Select the benchmark index for RS calculation",
        )
        st.session_state.benchmark = benchmark

        st.caption("📊 RS Calculation Periods")

        col1, col2, col3 = st.columns(3)

        with col1:
            rs1 = st.number_input(
                "Period 1",
                min_value=5,
                max_value=100,
                value=st.session_state.get("rs_period_1", 21),
                key="sector_rs1",
                help="Short-term RS (days)",
            )
            st.caption("Short")
            st.session_state.rs_period_1 = rs1

        with col2:
            rs2 = st.number_input(
                "Period 2",
                min_value=5,
                max_value=200,
                value=st.session_state.get("rs_period_2", 55),
                key="sector_rs2",
                help="Medium-term RS (days)",
            )
            st.caption("Medium")
            st.session_state.rs_period_2 = rs2

        with col3:
            rs3 = st.number_input(
                "Period 3",
                min_value=5,
                max_value=300,
                value=st.session_state.get("rs_period_3", 123),
                key="sector_rs3",
                help="Long-term RS (days)",
            )
            st.caption("Long")
            st.session_state.rs_period_3 = rs3

        st.divider()

        enable_audit = st.checkbox(
            "📋 Enable Audit Trail",
            value=st.session_state.get("enable_audit", True),
            key="sector_audit",
            help="Save analysis snapshots to audit logs",
        )
        st.session_state.enable_audit = enable_audit

        st.divider()

        # ACTION BUTTONS (ADMIN ONLY)
        if st.session_state.get("user_role") == "admin":
            analyze_clicked = st.button(
                "🔍 Analyze All Sectors",
                type="primary",
                width="stretch",
                key="sector_analyze_btn",
            )
            etf_clicked = st.button(
                "📑 Calculate ETF RS",
                type="secondary",
                width="stretch",
                key="sector_etf_btn",
            )

            if analyze_clicked:
                if not st.session_state.admin_connected:
                    st.error("❌ Please connect to AngelOne first")
                else:
                    from rs_analyzer import SectorRSAnalyzer
                    from config import SECTOR_TOKENS, BENCHMARK_TOKENS

                    connector = st.session_state.admin_connector
                    benchmark_name = st.session_state.get("benchmark", "NIFTY 50")
                    rs1 = st.session_state.get("rs_period_1", 21)
                    rs2 = st.session_state.get("rs_period_2", 55)
                    rs3 = st.session_state.get("rs_period_3", 123)

                    with st.spinner("Analyzing all sectors..."):
                        analyzer = SectorRSAnalyzer(connector, SECTOR_TOKENS)
                        df = analyzer.analyze(
                            BENCHMARK_TOKENS[benchmark_name]["token"],
                            [rs1, rs2, rs3],
                            None,
                        )

                    if df is None or df.empty:
                        st.error("❌ No sector data returned")
                    else:
                        st.session_state.analysis_results = df
                        st.session_state.last_analysis_time = datetime.now()
                        try:
                            df.to_csv("sector_analysis_data.csv", index=False)
                            st.success("✅ Sector analysis complete and saved")
                        except Exception as e:
                            st.warning(f"⚠️ Analysis done but save failed: {e}")

            if etf_clicked:
                if not st.session_state.admin_connected:
                    st.error("❌ Please connect to AngelOne first")
                else:
                    from etf_rs_calculator import calculate_etf_rs

                    smartapi = st.session_state.admin_connector.smartapi
                    with st.spinner("Calculating ETF RS for all ETFs..."):
                        df_etf = calculate_etf_rs(
                            smartapi, "ETFs-List_updated.csv"
                        )

                    if df_etf is None or df_etf.empty:
                        st.error("❌ No ETF data returned")
                    else:
                        st.session_state.etf_rs = df_etf
                        st.session_state.last_etf_time = datetime.now()
                        try:
                            df_etf.to_csv("etf_rs_output.csv", index=False)
                            st.success("✅ ETF RS calculation complete and saved")
                        except Exception as e:
                            st.warning(f"⚠️ ETF RS done but save failed: {e}")
        else:
            st.info("💡 Only admin can refresh analysis.")

    # ===================================================================== #
    # MAIN CONTENT AREA
    # ===================================================================== #
    st.subheader("📊 Sector Relative Strength Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Benchmark", st.session_state.get("benchmark", "NIFTY 50"))

    with col2:
        rs_periods = (
            f"{st.session_state.rs_period_1}/"
            f"{st.session_state.rs_period_2}/"
            f"{st.session_state.rs_period_3}"
        )
        st.metric("RS Periods", rs_periods)

    with col3:
        if st.session_state.get("last_analysis_time"):
            st.metric(
                "Last Update",
                st.session_state.last_analysis_time.strftime("%H:%M IST"),
            )
        else:
            st.metric("Last Update", "Not yet")

    with col4:
        status = "🟢 Connected" if st.session_state.admin_connected else "🔴 Not Connected"
        st.metric("API Status", status)

    st.divider()

    if st.session_state.get("analysis_results") is not None:
        df = st.session_state.analysis_results

        st.write(f"**Sectors Analyzed:** {len(df)}")

        st.dataframe(df, width="stretch", hide_index=False)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 RS Distribution")
            if "RS1" in df.columns:
                st.bar_chart(df["RS1"].astype(float))

        with col2:
            st.subheader("🏆 Top Performing Sectors")
            if "RS1" in df.columns and "Sector" in df.columns:
                top_sectors = df.nlargest(5, "RS1")[["Sector", "RS1"]]
                st.dataframe(top_sectors, width="stretch", hide_index=True)

        st.divider()

        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sector Analysis (CSV)",
            data=csv,
            file_name=f"sector_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            width="stretch",
        )

    else:
        st.info("📊 No sector analysis data available yet.")
        st.write(
            "Admin: Click **'Analyze All Sectors'** in sidebar or Data Refresh tab to fetch live data."
        )
        st.write("Subscriber: Wait for admin to refresh the data.")

        st.divider()
        st.subheader("📋 Sample Data Structure")

        sample_df = pd.DataFrame(
            {
                "Sector": ["IT", "Banking", "Auto", "Pharma", "Energy"],
                "LTP": [15234.50, 42103.20, 8954.75, 28340.15, 18295.40],
                "Change %": [2.34, -1.20, 0.85, 1.45, -0.60],
                "RS1 (21d)": [65, 45, 55, 72, 38],
                "RS2 (55d)": [58, 42, 50, 68, 35],
                "RS3 (123d)": [61, 44, 48, 70, 37],
                "TLDR": ["Strong", "Weak", "Neutral", "Very Strong", "Weak"],
            }
        )

        st.dataframe(sample_df, width="stretch", hide_index=True)


if __name__ == "__main__":
    render_tab_sectors()
