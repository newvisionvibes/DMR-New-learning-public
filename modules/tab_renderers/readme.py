# ============================================================================
# FILE: modules/tab_renderers/readme.py
# ============================================================================

"""
README Tab Renderer
Help documentation
"""

import streamlit as st
from readme_content import render_readme_tab


def render_tab_readme():
    """Render README tab"""
    st.header("📚 Help Documentation")
    render_readme_tab()