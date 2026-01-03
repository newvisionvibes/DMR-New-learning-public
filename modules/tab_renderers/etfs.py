"""
Enhanced ETFs Tab Renderer - With Sidebar AngelOne & Analysis Settings
Fly.io Deployment Ready - V7
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")


def render_tab_etfs():
    """Render ETFs analysis tab with sidebar configuration"""

    # ===================================================================== #
    # SIDEBAR CONFIGURATION
    # ===================================================================== #
    with st.sidebar:
        st.header("⚙️ Configuration")

        # AngelOne API status
        if st.session_state.get("user_role") == "admin":
            with st.expander(
                "🔐 AngelOne API", expanded=not st.session_state.admin_connected
            ):
                if st.session_state.admin_connected:
                    st.success("✅ Connected to AngelOne")
                else:
                    st.warning("⚠️ Not connected")
                    st.caption("Use main sidebar to connect")
        else:
            st.info("🔐 Connection managed by administrator")

        st.divider()

        # ETF analysis settings
        st.header("📈 ETF Analysis Settings")

        etf_category = st.multiselect(
            "ETF Categories",
            options=[
                "Broad Market",
                "Banking",
                "IT",
                "Pharma",
                "Commodities",
                "Debt",
            ],
            default=["Broad Market", "Banking"],
            key="etf_categories",
        )

        st.caption("📊 RS Calculation Periods")

        col1, col2, col3 = st.columns(3)

        with col1:
            rs1 = st.number_input(
                "Period 1",
                min_value=5,
                max_value=100,
                value=st.session_state.get("rs_period_1", 21),
                key="etf_rs1",
                help="Short-term RS",
            )
            st.caption("Short")
            st.session_state.rs_period_1 = rs1

        with col2:
            rs2 = st.number_input(
                "Period 2",
                min_value=5,
                max_value=200,
                value=st.session_state.get("rs_period_2", 55),
                key="etf_rs2",
                help="Medium-term RS",
            )
            st.caption("Medium")
            st.session_state.rs_period_2 = rs2

        with col3:
            rs3 = st.number_input(
                "Period 3",
                min_value=5,
                max_value=300,
                value=st.session_state.get("rs_period_3", 123),
                key="etf_rs3",
                help="Long-term RS",
            )
            st.caption("Long")
            st.session_state.rs_period_3 = rs3

        st.divider()

        sort_by = st.selectbox(
            "Sort By",
            options=[
                "RS1 (Strong to Weak)",
                "LTP (High to Low)",
                "Change % (Best to Worst)",
            ],
            key="etf_sort",
            help="How to order ETF results",
        )

        st.divider()

        enable_audit = st.checkbox(
            "📋 Enable Audit Trail",
            value=st.session_state.get("enable_audit", True),
            key="etf_audit",
        )
        st.session_state.enable_audit = enable_audit

        st.divider()

        if st.session_state.get("user_role") == "admin":
            if st.button(
                "📑 Calculate ETF RS",
                type="primary",
                width="stretch",
                key="etf_calc_btn",
            ):
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
            st.info("💡 Only admin can refresh ETF analysis")

    # ===================================================================== #
    # MAIN CONTENT AREA
    # ===================================================================== #
    st.subheader("💼 ETF Relative Strength Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        cats = st.session_state.get("etf_categories", etf_category) or ["All"]
        cats_str = ", ".join(cats)
        if len(cats_str) > 20:
            cats_str = cats_str[:20] + "..."
        st.metric("Categories", cats_str)

    with col2:
        rs_periods = (
            f"{st.session_state.rs_period_1}/"
            f"{st.session_state.rs_period_2}/"
            f"{st.session_state.rs_period_3}"
        )
        st.metric("RS Periods", rs_periods)

    with col3:
        if st.session_state.get("last_etf_time"):
            st.metric(
                "Last ETF Update",
                st.session_state.last_etf_time.strftime("%H:%M IST"),
            )
        else:
            st.metric("Last ETF Update", "Not yet")

    with col4:
        status = "🟢 Connected" if st.session_state.admin_connected else "🔴 Not Connected"
        st.metric("API Status", status)

    st.divider()

    if st.session_state.get("etf_rs") is not None:
        df = st.session_state.etf_rs.copy()

        # Apply category filter if column exists
        if "Category" in df.columns and etf_category:
            df = df[df["Category"].isin(etf_category)]

        # Sorting
        if "RS1" in df.columns and sort_by.startswith("RS1"):
            df = df.sort_values("RS1", ascending=False)
        elif "LTP" in df.columns and sort_by.startswith("LTP"):
            df = df.sort_values("LTP", ascending=False)
        elif "Change %" in df.columns and sort_by.startswith("Change"):
            df = df.sort_values("Change %", ascending=False)

        st.write(f"**ETFs Shown:** {len(df)}")

        st.dataframe(df, width="stretch", hide_index=False)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📈 RS Distribution")
            if "RS1" in df.columns:
                st.bar_chart(df["RS1"].astype(float).head(15))

        with col2:
            st.subheader("🏆 Top ETFs by RS")
            if "RS1" in df.columns and "ETF_Name" in df.columns:
                top_etfs = df.nlargest(5, "RS1")[["ETF_Name", "RS1"]]
                if "Change %" in df.columns:
                    top_etfs["Change %"] = df.nlargest(5, "RS1")["Change %"]
                st.dataframe(top_etfs, width="stretch", hide_index=True)

        st.divider()

        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download ETF Analysis (CSV)",
            data=csv,
            file_name=f"etf_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            width="stretch",
        )

    else:
        st.info("💼 No ETF analysis data available yet.")
        st.write(
            "Admin: Click **'Calculate ETF RS'** in sidebar or Data Refresh tab to fetch live data."
        )
        st.write("Subscriber: Wait for admin to refresh the data.")

        st.divider()
        st.subheader("📋 Sample ETF Data Structure")

        sample_df = pd.DataFrame(
            {
                "ETF_Name": [
                    "Nifty 50 ETF",
                    "Bank ETF",
                    "IT ETF",
                    "Gold ETF",
                    "Sensex ETF",
                ],
                "Category": [
                    "Broad Market",
                    "Banking",
                    "IT",
                    "Commodities",
                    "Broad Market",
                ],
                "LTP": [8234.50, 5103.20, 3954.75, 6340.15, 7295.40],
                "Change %": [1.20, -0.80, 0.45, 1.85, 0.95],
                "RS1 (21d)": [68, 52, 78, 45, 65],
                "RS2 (55d)": [62, 48, 72, 40, 58],
                "RS3 (123d)": [65, 50, 75, 42, 61],
                "TLDR": ["Strong", "Neutral", "Very Strong", "Weak", "Strong"],
            }
        )

        st.dataframe(sample_df, width="stretch", hide_index=True)

        st.subheader("📊 Sample Category Breakdown")

        category_data = pd.DataFrame(
            {
                "Category": [
                    "Broad Market",
                    "Banking",
                    "IT",
                    "Commodities",
                    "Debt",
                ],
                "ETF Count": [5, 8, 6, 4, 3],
                "Avg RS1": [65, 50, 72, 45, 55],
            }
        )

        st.dataframe(category_data, width="stretch", hide_index=True)


if __name__ == "__main__":
    render_tab_etfs()
