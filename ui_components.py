# ui_components.py
"""
UI Components Module
Styling and formatting utilities for Streamlit interface
"""

import pandas as pd

def get_color_for_rs(rs_value):
    """Return CSS color style for RS value"""
    if rs_value >= 3:
        return "background-color: #166534; color: white"
    elif rs_value >= 1.5:
        return "background-color: #22c55e; color: white"
    elif rs_value >= 0:
        return "background-color: #86efac; color: black"
    elif rs_value >= -1.5:
        return "background-color: #fca5a5; color: black"
    elif rs_value <= -3:
        return "background-color: #ef4444; color: white"
    else:
        return "background-color: #991b1b; color: white"

def get_color_for_pct_change(pct_value):
    """Return CSS color style for percentage change"""
    if pct_value >= 1:
        return "background-color: #22c55e; color: white"
    elif pct_value >= 0:
        return "background-color: #86efac; color: black"
    elif pct_value >= -1:
        return "background-color: #fca5a5; color: black"
    else:
        return "background-color: #ef4444; color: white"

def get_color_for_pct_20dma(pct_value):
    """Return CSS color style for 20-DMA change"""
    if pd.isna(pct_value):
        return ""
    
    if pct_value >= 0:
        return "background-color: #86efac; color: black"
    else:
        return "background-color: #fca5a5; color: black"

def classify_etf_strategy(row):
    """Classify ETF for trading strategy based on metrics"""
    rs21 = row.get("RS21", 0)
    rs55 = row.get("RS55", 0)
    rs123 = row.get("RS123", 0)
    pct_change = row.get("Change", 0)
    pct_20dma = row.get("Change 20 DMA", 0)
    
    strategies = []
    
    # Intraday strategy
    if pct_change > 0.3 and rs21 > 1 and pct_20dma > 0:
        strategies.append("Intraday")
    
    # Swing strategy
    if rs55 > 1 and pct_20dma > 0.5 and rs21 > 0:
        strategies.append("Swing")
    
    # Long-term strategy
    if rs55 > 2 and rs123 > 1 and pct_20dma > 1:
        strategies.append("Long-term")
    
    return " | ".join(strategies) if strategies else "Consolidating"

def style_dataframe(df, rs_columns, pct_columns=None):
    """Apply styling to dataframe for display"""
    if pct_columns is None:
        pct_columns = ["Change"]
    
    styled = df.style.applymap(
        get_color_for_rs, 
        subset=rs_columns
    ).applymap(
        get_color_for_pct_change, 
        subset=pct_columns
    )
    
    return styled

def create_metric_box(label, value, color="primary"):
    """Create a metric box for display"""
    colors = {
        "primary": "#667eea",
        "success": "#10b981",
        "danger": "#ef4444"
    }
    color_code = colors.get(color, colors["primary"])
    return f"""
    <div style="background-color: #f9fafb; border-left: 4px solid {color_code}; 
                padding: 15px; border-radius: 4px; margin: 5px 0;">
        <div style="font-size: 12px; color: #666; text-transform: uppercase; 
                    letter-spacing: 0.5px;">{label}</div>
        <div style="font-size: 24px; font-weight: bold; color: #333; margin-top: 5px;">
            {value}</div>
    </div>
    """
