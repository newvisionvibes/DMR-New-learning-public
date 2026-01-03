import streamlit as st

def render_global_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")

        role = st.session_state.get("user_role")

        if role == "admin":
            st.success("👑 Admin Mode")
            st.caption("Manage data refresh & analysis")

            st.divider()

            st.button("🔍 Analyze All Sectors", width="stretch")
            st.button("🧮 Analyze ETFs", width="stretch")
            st.button("📊 Analyze Both", width="stretch")

        else:
            st.info("📘 Learning Mode")
            st.caption("Data refreshed by admin")

        st.divider()

        st.caption("📌 Educational Edition")
