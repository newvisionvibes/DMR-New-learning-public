"""
HOME TAB – Subscriber Welcome & Objectives
Aligned with 'ETF Market Analysis SaaS – Project & Deployment Document V6'
Pure informational page (no logic, no API calls)
"""

import streamlit as st


def render_tab_home():
    """Render Home / Welcome tab"""

    st.header("🏠 Welcome to ETF Market Analysis")

    st.markdown(
        """
        ### 📌 What is this platform?

        **ETF Market Analysis** is a **data-driven analytical platform** designed to help
        investors and traders **understand relative strength trends** across:
        - Indian market sectors
        - Exchange Traded Funds (ETFs)

        This platform focuses on **market structure, momentum, and relative performance**
        — not stock tips or trade calls.
        """
    )

    st.divider()

    st.markdown(
        """
        ### 🎯 Core Objectives

        - Identify **strong vs weak sectors**
        - Track **ETF relative strength (RS) trends**
        - Support **informed decision-making**
        - Provide **clean, repeatable market insights**
        - Reduce emotional & noise-driven trading
        """
    )

    st.divider()

    st.markdown(
        """
        ### 👥 Who is this for?

        ✅ Swing traders  
        ✅ Positional traders  
        ✅ Long-term investors  
        ✅ Market learners & analysts  

        ### 🚫 Who this is NOT for?

        ❌ Intraday scalpers  
        ❌ Telegram tip followers  
        ❌ Guaranteed-return seekers  
        ❌ High-frequency traders  
        """
    )

    st.divider()

    st.markdown(
        """
        ### 🔄 How the data works

        - Data is fetched from **Angel One SmartAPI**
        - Refresh happens **periodically during market hours**
        - **Same data is shown to all users**
        - No per-user data fetching (safe & reliable)
        - Last refresh time is shown on each dashboard
        """
    )

    st.divider()

    st.markdown(
        """
        ### ⚠️ Important Disclaimer

        - This platform is for **educational & analytical purposes only**
        - It does **NOT** provide buy/sell recommendations
        - It is **NOT** investment advice
        - Users are responsible for their own decisions
        - Markets involve risk — please trade responsibly
        """
    )

    st.info(
        "💡 Tip: Start with the **ETFs RS** tab to see relative strength trends, "
        "then explore **Sectors** for broader market context."
    )
