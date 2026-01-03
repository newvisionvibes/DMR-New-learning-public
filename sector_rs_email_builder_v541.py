"""
sector_rs_email_builder_v541_enhanced.py

MODULE PURPOSE: EDUCATIONAL & INFORMATIONAL ONLY
Email report builder for generating educational analysis summaries.

Learning Objectives:
- Understand how to create HTML email templates
- Learn email automation concepts
- Study report generation techniques
- Explore professional communication formatting

Features:
✅ Top 5 & Bottom 5 Sector Performers with % Change 20 DMA
✅ Top 5 & Bottom 5 ETF Performers with % Change 20 DMA
✅ Comprehensive market analysis email
✅ Educational disclaimers & educational POV text
✅ Professional formatting

NOT FOR: Financial advice, trading signals, or investment recommendations

COMPLIANCE: SEBI/RBI Educational Use Only - Version 5.4.1 Enhanced

EDUCATIONAL FOCUS:
This module teaches how to create automated reports and email
communications. It's a learning tool for understanding HTML email
generation and professional report formatting.

DISCLAIMER:
This module is for educational purposes only. The reports generated
are educational content, NOT investment advice. Users must conduct
independent research and consult qualified financial advisors.
"""

import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _fmt(val, is_pct: bool = False) -> str:
    """Format value for display - EDUCATIONAL"""
    if pd.isna(val):
        return "-"
    try:
        v = float(val)
    except Exception:
        return str(val)
    
    if is_pct:
        sign = "+" if v > 0 else ""
        return f"{sign}{v:.2f}%"
    return f"{v:,.2f}"


def _table_html(
    df: pd.DataFrame,
    cols,
    title: str,
    limit: int = 5,
    zebra_color: str | None = None,
) -> str:
    """Create professional HTML table from DataFrame - EDUCATIONAL"""
    if df.empty:
        return ""
    
    df = df[cols].copy().head(limit)
    
    html = f"\n<h3 style='margin-top:18px;margin-bottom:8px;'>{title}</h3>"
    html += "<table style='width:100%;border-collapse:collapse;margin:8px 0;font-size:13px;'>"
    html += "<thead><tr style='background:#f2f2f2;'>"
    
    # Add header row
    for i, c in enumerate(cols):
        html += f"<th style='padding:6px 8px;border:1px solid #ddd;'>{c}</th>"
    html += "</tr></thead><tbody>"
    
    # Add data rows
    row_num = 1
    for _, row in df.iterrows():
        bg = zebra_color if zebra_color and row_num % 2 == 1 else "#ffffff"
        html += f"<tr style='background:{bg};'>"
        
        for c in cols:
            v = row.get(c, None)
            is_pct = any(x in c for x in ["RS_", "Change", "%"])
            txt = _fmt(v, is_pct)
            
            color = ""
            if is_pct and isinstance(v, (int, float)):
                if v > 0:
                    color = "color:#198754;font-weight:600;"
                elif v < 0:
                    color = "color:#dc3545;font-weight:600;"
            
            html += f"<td style='padding:6px 8px;border:1px solid #ddd;{color}'>{txt}</td>"
        
        html += "</tr>"
        row_num += 1
    
    html += "</tbody></table>"
    return html


def _full_sector_table(df: pd.DataFrame) -> str:
    """Create full sector analysis table - EDUCATIONAL"""
    if df.empty:
        return ""
    
    base_cols = ["Sector", "LTP", "Change", "% Change 20 DMA", "RS_21", "RS_55", "RS_123", "Category", "TLDR"]
    cols = [c for c in base_cols if c in df.columns]
    
    if not cols:
        return ""
    
    view = df[cols].copy()
    
    html = (
        "<h3 style='margin-top:24px;margin-bottom:8px;'>"
        "Complete Sector RS Analysis (Research View)</h3>"
        "<table style='width:100%;border-collapse:collapse;margin:8px 0;"
        "font-size:12px;'>"
        "<thead><tr style='background:#f2f2f2;'>"
    )
    
    for c in cols:
        html += f"<th style='padding:6px 8px;border:1px solid #ddd;'>{c}</th>"
    
    html += "</tr></thead><tbody>"
    
    rs_cols = [c for c in ["RS_21", "RS_55", "RS_123"] if c in cols]
    
    for _, row in view.iterrows():
        html += "<tr>"
        for c in cols:
            v = row.get(c, None)
            is_pct = any(x in c for x in ["RS_", "Change", "%"])
            txt = _fmt(v, is_pct)
            
            cell_style = "padding:5px 6px;border:1px solid #ddd;text-align:center;"
            
            if c in rs_cols and pd.notna(v):
                try:
                    val = float(v)
                except Exception:
                    val = 0.0
                
                if val >= 3:
                    bg = "#c6f6d5"
                elif val >= 1:
                    bg = "#e6ffed"
                elif val <= -3:
                    bg = "#fed7d7"
                elif val < -1:
                    bg = "#fbe9eb"
                else:
                    bg = "#ffffff"
                cell_style += f"background:{bg};"
            
            html += f"<td style='{cell_style}'>{txt}</td>"
        
        html += "</tr>"
    
    html += "</tbody></table>"
    return html


def _full_etf_table(df: pd.DataFrame) -> str:
    """Create full ETF analysis table - EDUCATIONAL"""
    if df.empty:
        return ""
    
    base_cols = ["ETF Code", "LTP", "% Change", "% Change 20 DMA", "RS_21", "RS_55", "RS_123", "Strategy"]
    cols = [c for c in base_cols if c in df.columns]
    
    if not cols:
        return ""
    
    view = df[cols].copy()
    
    html = (
        "<h3 style='margin-top:24px;margin-bottom:8px;'>"
        "Complete ETF RS Analysis (Research View)</h3>"
        "<table style='width:100%;border-collapse:collapse;margin:8px 0;"
        "font-size:12px;'>"
        "<thead><tr style='background:#f2f2f2;'>"
    )
    
    for c in cols:
        html += f"<th style='padding:6px 8px;border:1px solid #ddd;'>{c}</th>"
    
    html += "</tr></thead><tbody>"
    
    rs_cols = [c for c in ["RS_21", "RS_55", "RS_123"] if c in cols]
    
    for _, row in view.iterrows():
        html += "<tr>"
        for c in cols:
            v = row.get(c, None)
            is_pct = any(x in c for x in ["RS_", "Change", "%"])
            txt = _fmt(v, is_pct)
            
            cell_style = "padding:5px 6px;border:1px solid #ddd;text-align:center;"
            
            if c in rs_cols and pd.notna(v):
                try:
                    val = float(v)
                except Exception:
                    val = 0.0
                
                if val >= 3:
                    bg = "#c6f6d5"
                elif val >= 1:
                    bg = "#e6ffed"
                elif val <= -3:
                    bg = "#fed7d7"
                elif val < -1:
                    bg = "#fbe9eb"
                else:
                    bg = "#ffffff"
                cell_style += f"background:{bg};"
            
            html += f"<td style='{cell_style}'>{txt}</td>"
        
        html += "</tr>"
    
    html += "</tbody></table>"
    return html


def _html_head() -> str:
    """HTML header for emails - EDUCATIONAL"""
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <style>
        body {
            font-family: Segoe UI, Arial, sans-serif;
            background: #f5f5f5;
            color: #333;
        }
        .wrap {
            max-width: 900px;
            margin: 0 auto;
            background: #fff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 22px 24px;
            text-align: center;
        }
        .hero h1 {
            margin: 0;
            font-size: 24px;
            font-weight: 400;
        }
        .hero p {
            margin: 4px 0 0 0;
            font-size: 12px;
            opacity: .9;
        }
        h2 {
            margin-top: 22px;
            border-bottom: 2px solid #228ae6;
            padding-bottom: 6px;
            font-size: 18px;
        }
        h3 {
            font-size: 15px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 6px 8px;
            text-align: center;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        .disclaimer-box {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 4px solid #228ae6;
            font-size: 13px;
            line-height: 1.5;
        }
        .disclaimer-box h3 {
            margin-top: 0;
            color: #228ae6;
        }
        .disclaimer-box ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .disclaimer-box li {
            margin: 5px 0;
        }
    </style>
</head>
<body>
<div class='wrap'>
"""


def _html_foot() -> str:
    """HTML footer for emails - EDUCATIONAL"""
    return """
    </div>
</body>
</html>

<p style='font-size:11px;color:#666;padding:10px 14px;border-top:1px solid #eee;margin-top:16px;'>
Generated: """ + datetime.now().strftime('%Y-%m-%d %H:%M IST') + """ | Data Source: Public Markets | Educational Use Only
</p>
"""


def _comprehensive_disclaimer() -> str:
    """Comprehensive disclaimer for market analysis emails"""
    return """
    <div class='disclaimer-box'>
        <h3>📚 Comprehensive Disclaimer</h3>
        
        <p><strong>This comprehensive report combines educational analysis across multiple asset classes. 
        It is designed to help readers practice cross-asset comparison and relative strength interpretation for learning purposes.</strong></p>
        
        <h4 style='margin-top:12px;margin-bottom:6px;'>What this report is:</h4>
        <ul>
            <li>Not a portfolio recommendation or asset allocation strategy</li>
            <li>Not investment advice or a solicitation to invest</li>
            <li>Not a substitute for professional financial guidance</li>
            <li>Not suitable on its own for making investment decisions without further research</li>
        </ul>
        
        <p style='margin:12px 0;font-size:12px;'>
        <strong>Important:</strong> Market analysis requires consideration of multiple factors including your risk tolerance, 
        time horizon, liquidity needs, tax situation, and investment objectives. Always conduct thorough due diligence and 
        consult qualified professionals before making investment decisions.
        </p>
        
        <p style='margin:12px 0;font-size:12px;color:#666;'>
        <strong>Data Notes:</strong> Market prices are from public sources and current as of the report generation time. 
        Past performance is not indicative of future results.
        </p>
    </div>
    """


def _sector_disclaimer() -> str:
    """Sector-specific educational disclaimer"""
    return """
    <div class='disclaimer-box'>
        <h3>📊 Sector Analysis – Learning Overview</h3>
        
        <p><strong>Purpose:</strong> This email shares an educational snapshot of recent sector behaviour using relative 
        strength (RS) metrics. It is prepared for learning and discussion purposes only, to help readers practice reading 
        market data independently.</p>
        
        <p><strong>This email is provided for educational and informational purposes only.</strong> It illustrates how to read 
        relative strength metrics, price movements, and simple comparative statistics so that readers can practice their own 
        independent market analysis.</p>
        
        <h4 style='margin-top:12px;margin-bottom:6px;'>This content is:</h4>
        <ul>
            <li>Not a personal investment recommendation</li>
            <li>Not a solicitation to buy, sell, or hold any security</li>
            <li>Not a substitute for professional financial advice</li>
            <li>Not an endorsement of any particular strategy or product</li>
        </ul>
        
        <p style='margin:12px 0;font-size:12px;'>
        <strong>Always remember:</strong> Past performance does not guarantee future results. Market data comes from publicly 
        available sources and is intended for learning purposes. Always conduct your own due diligence and 
        <strong>consult qualified advisors before making financial decisions.</strong>
        </p>
    </div>
    """


def _etf_disclaimer() -> str:
    """ETF-specific educational disclaimer"""
    return """
    <div class='disclaimer-box'>
        <h3>💼 ETF Analysis – Learning Case Study</h3>
        
        <p><strong>Purpose:</strong> This email presents ETF data and relative strength analysis as an educational case study. 
        It is designed to help readers practice comparing investment vehicles using quantitative metrics, without making 
        investment recommendations.</p>
        
        <p><strong>The ETF information in this email is presented as an educational case study in relative strength analysis 
        and comparative metrics. It should NOT be used on its own to make investment decisions.</strong></p>
        
        <h4 style='margin-top:12px;margin-bottom:6px;'>Important Learning Considerations:</h4>
        <ul>
            <li>This analysis does not take into account your financial situation, objectives, or needs</li>
            <li>ETF selection requires evaluation of fees, holdings, tax efficiency, and diversification</li>
            <li>Past relative strength does not predict future performance</li>
            <li>Market data is from public sources and subject to change</li>
        </ul>
        
        <p style='margin:12px 0;font-size:12px;'>
        This email is intended to help you understand and practice quantitative analysis techniques. 
        <strong>Before investing, consult with a qualified financial advisor who understands your complete financial situation.</strong>
        </p>
    </div>
    """


def generate_comprehensive_newsletter_v541(
    sector_df: pd.DataFrame,
    etf_df: pd.DataFrame,
    benchmark: str = "NIFTY 50",
) -> str:
    """
    Generate comprehensive market analysis email with Top 5 & Bottom 5 performers
    
    EDUCATIONAL CONTENT ONLY - NOT FOR INVESTMENT DECISIONS
    
    Features:
    ✅ Top 5 Performing Sectors with % Change 20 DMA
    ✅ Bottom 5 Underperforming Sectors with % Change 20 DMA
    ✅ Top 5 Leading ETFs with % Change 20 DMA
    ✅ Bottom 5 Lagging ETFs with % Change 20 DMA
    ✅ Full research tables
    ✅ Comprehensive educational disclaimers
    
    Args:
        sector_df: Sector analysis DataFrame
        etf_df: ETF analysis DataFrame
        benchmark: Benchmark name (default: NIFTY 50)
    
    Returns:
        str: Complete HTML email content
    """
    
    # ✅ FIX: Convert all RS and Change columns to numeric types
    sector_df = sector_df.copy()
    etf_df = etf_df.copy()
    
    for col in ['RS_21', 'RS_55', 'RS_123', 'Change', '% Change', '% Change 20 DMA', 'LTP']:
        if col in sector_df.columns:
            sector_df[col] = pd.to_numeric(sector_df[col], errors='coerce')
        if col in etf_df.columns:
            etf_df[col] = pd.to_numeric(etf_df[col], errors='coerce')
    
    html = _html_head()
    html += (
        "<div class='hero'>"
        "<h1>📈 Comprehensive Market Analysis</h1>"
        "<p>Sectors &amp; ETFs | Relative Strength Study</p>"
        f"<p style='font-size:11px;margin:8px 0 0 0;'>Benchmark: {benchmark} · "
        f"{datetime.now().strftime('%Y-%m-%d')}</p>"
        "</div>"
        "<div style='padding:16px 18px;'>"
    )

    html += (
        "<p style='font-size:13px;color:#666;background:#f0f4f8;padding:12px;border-radius:6px;margin:10px 0;'>"
        "<strong>Purpose:</strong> This comprehensive report combines sector and ETF relative strength analysis to illustrate "
        "how multiple asset classes can be compared using common metrics. It is prepared for educational discussion and learning, "
        "<strong>not as actionable advice.</strong></p>"
    )

    if not sector_df.empty:
        html += "<h2>Sectors</h2>"
        total = len(sector_df)
        outp = (
            len(sector_df[sector_df.get("Category") == "Outperforming"])
            if "Category" in sector_df.columns
            else 0
        )
        mixed = (
            len(sector_df[sector_df.get("Category") == "Mixed"])
            if "Category" in sector_df.columns
            else 0
        )
        under = (
            len(sector_df[sector_df.get("Category") == "Underperforming"])
            if "Category" in sector_df.columns
            else 0
        )
        avg_rs = (
            sector_df["RS_55"].mean() if "RS_55" in sector_df.columns else 0.0
        )

        html += (
            "<table style='width:100%;border-collapse:collapse;margin:14px 0;"
            "font-size:13px;'><tr>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;'><b>{total}</b><br>"
            "Total Sectors</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#198754;'>"
            f"<b>{outp}</b><br>Outperforming</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#ffc107;'>"
            f"<b>{mixed}</b><br>Mixed</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#dc3545;'>"
            f"<b>{under}</b><br>Underperforming</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#0d6efd;'>"
            f"<b>{_fmt(avg_rs, True)}</b><br>Avg RS‑55</td>"
            "</tr></table>"
        )

        if "RS_55" in sector_df.columns:
            has_pct_20_dma = "% Change 20 DMA" in sector_df.columns
            
            if has_pct_20_dma:
                cols = ["Sector", "LTP", "Change", "% Change 20 DMA", "RS_55"]
                out_cols = ["Name", "LTP", "Change", "% Chg 20‑DMA", "RS_55"]
            else:
                cols = ["Sector", "LTP", "Change", "RS_55"]
                out_cols = ["Name", "LTP", "Change", "RS_55"]

            top_sec = sector_df.nlargest(5, "RS_55")[cols].copy()
            top_sec.columns = out_cols
            html += _table_html(
                top_sec,
                out_cols,
                "Top 5 Performing Sectors",
                limit=5,
                zebra_color="#e6f4ea",
            )

            bottom_sec = sector_df.nsmallest(5, "RS_55")[cols].copy()
            bottom_sec.columns = out_cols
            html += _table_html(
                bottom_sec,
                out_cols,
                "Bottom 5 Underperforming Sectors",
                limit=5,
                zebra_color="#fbe9eb",
            )

        html += _full_sector_table(sector_df)

    if not etf_df.empty:
        html += "<h2>ETFs</h2>"
        total = len(etf_df)
        # ✅ FIX: Convert RS_55 to numeric before comparison
        leaders = (
            len(etf_df[etf_df["RS_55"] > 0].dropna()) if "RS_55" in etf_df.columns else 0
        )

        html += (
            "<table style='width:100%;border-collapse:collapse;margin:14px 0;"
            "font-size:13px;'><tr>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;'><b>{total}</b><br>"
            "Total ETFs</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#198754;'>"
            f"<b>{leaders}</b><br>Leaders (RS‑55 > 0)</td>"
            "</tr></table>"
        )

        if "RS_55" in etf_df.columns:
            has_pct_20_dma = "% Change 20 DMA" in etf_df.columns
            
            if has_pct_20_dma:
                cols = ["ETF Code", "LTP", "% Change", "% Change 20 DMA", "RS_55"]
                out_cols = ["Name", "LTP", "Change", "% Chg 20‑DMA", "RS_55"]
            else:
                cols = ["ETF Code", "LTP", "% Change", "RS_55"]
                out_cols = ["Name", "LTP", "Change", "RS_55"]

            top_etf = etf_df.nlargest(5, "RS_55")[cols].copy()
            top_etf.columns = out_cols
            html += _table_html(
                top_etf,
                out_cols,
                "Top 5 Leading ETFs",
                limit=5,
                zebra_color="#e6f4ea",
            )

            bottom_etf = etf_df.nsmallest(5, "RS_55")[cols].copy()
            bottom_etf.columns = out_cols
            html += _table_html(
                bottom_etf,
                out_cols,
                "Bottom 5 Lagging ETFs",
                limit=5,
                zebra_color="#fbe9eb",
            )

        html += _full_etf_table(etf_df)

    html += _comprehensive_disclaimer()
    html += "</div>" + _html_foot()
    return html


def generate_sector_newsletter_v541(
    sector_df: pd.DataFrame,
    benchmark: str = "NIFTY 50",
) -> str:
    """Generate sector-only newsletter with Top 5 & Bottom 5 - EDUCATIONAL"""
    
    # ✅ FIX: Convert RS and Change columns to numeric types
    sector_df = sector_df.copy()
    for col in ['RS_21', 'RS_55', 'RS_123', 'Change', '% Change', '% Change 20 DMA', 'LTP']:
        if col in sector_df.columns:
            sector_df[col] = pd.to_numeric(sector_df[col], errors='coerce')
    
    html = _html_head()
    html += (
        "<div class='hero'>"
        "<h1>📊 Sector Relative Strength Analysis</h1>"
        "<p>Educational snapshot of market metrics</p>"
        f"<p style='font-size:11px;margin:8px 0 0 0;'>Benchmark: {benchmark}</p>"
        "</div>"
        "<div style='padding:16px 18px;'>"
    )

    html += (
        "<p style='font-size:13px;color:#666;background:#f0f4f8;padding:12px;border-radius:6px;margin:10px 0;'>"
        "<strong>Purpose:</strong> This email shares an educational snapshot of recent sector behaviour using relative "
        "strength (RS) metrics. It is prepared for learning and discussion purposes only, to help readers practice reading "
        "market data independently.</p>"
    )

    if not sector_df.empty:
        html += "<h2>Sectors</h2>"
        total = len(sector_df)
        outp = len(sector_df[sector_df.get("Category") == "Outperforming"]) if "Category" in sector_df.columns else 0
        avg_rs = sector_df["RS_55"].mean() if "RS_55" in sector_df.columns else 0.0

        html += (
            "<table style='width:100%;border-collapse:collapse;margin:14px 0;font-size:13px;'><tr>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;'><b>{total}</b><br>Total Sectors</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#198754;'><b>{outp}</b><br>Outperforming</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#0d6efd;'><b>{_fmt(avg_rs, True)}</b><br>Avg RS‑55</td>"
            "</tr></table>"
        )

        if "RS_55" in sector_df.columns:
            has_pct_20_dma = "% Change 20 DMA" in sector_df.columns
            cols = ["Sector", "LTP", "Change", "% Change 20 DMA", "RS_55"] if has_pct_20_dma else ["Sector", "LTP", "Change", "RS_55"]
            out_cols = ["Name", "LTP", "Change", "% Chg 20‑DMA", "RS_55"] if has_pct_20_dma else ["Name", "LTP", "Change", "RS_55"]

            top_sec = sector_df.nlargest(5, "RS_55")[cols].copy()
            top_sec.columns = out_cols
            html += _table_html(top_sec, out_cols, "Top 5 Performing Sectors", limit=5, zebra_color="#e6f4ea")

            bottom_sec = sector_df.nsmallest(5, "RS_55")[cols].copy()
            bottom_sec.columns = out_cols
            html += _table_html(bottom_sec, out_cols, "Bottom 5 Underperforming Sectors", limit=5, zebra_color="#fbe9eb")

        html += _full_sector_table(sector_df)

    html += _sector_disclaimer()
    html += "</div>" + _html_foot()
    return html


def generate_etf_newsletter_v541(etf_df: pd.DataFrame) -> str:
    """Generate ETF-only newsletter with Top 5 & Bottom 5 - EDUCATIONAL"""
    
    # ✅ FIX: Convert RS and Change columns to numeric types
    etf_df = etf_df.copy()
    for col in ['RS_21', 'RS_55', 'RS_123', 'Change', '% Change', '% Change 20 DMA', 'LTP']:
        if col in etf_df.columns:
            etf_df[col] = pd.to_numeric(etf_df[col], errors='coerce')
    
    html = _html_head()
    html += (
        "<div class='hero'>"
        "<h1>💼 ETF Relative Strength Analysis</h1>"
        "<p>Educational comparison of ETF metrics</p>"
        "</div>"
        "<div style='padding:16px 18px;'>"
    )

    html += (
        "<p style='font-size:13px;color:#666;background:#f0f4f8;padding:12px;border-radius:6px;margin:10px 0;'>"
        "<strong>Purpose:</strong> This email presents ETF data and relative strength analysis as an educational case study. "
        "It is designed to help readers practice comparing investment vehicles using quantitative metrics, without making "
        "investment recommendations.</p>"
    )

    if not etf_df.empty:
        html += "<h2>ETFs</h2>"
        total = len(etf_df)
        # ✅ FIX: Convert RS_55 to numeric before comparison
        leaders = len(etf_df[etf_df["RS_55"] > 0].dropna()) if "RS_55" in etf_df.columns else 0

        html += (
            "<table style='width:100%;border-collapse:collapse;margin:14px 0;font-size:13px;'><tr>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;'><b>{total}</b><br>Total ETFs</td>"
            f"<td style='border:1px solid #ddd;padding:8px 10px;color:#198754;'><b>{leaders}</b><br>Leaders (RS‑55 > 0)</td>"
            "</tr></table>"
        )

        if "RS_55" in etf_df.columns:
            has_pct_20_dma = "% Change 20 DMA" in etf_df.columns
            cols = ["ETF Code", "LTP", "% Change", "% Change 20 DMA", "RS_55"] if has_pct_20_dma else ["ETF Code", "LTP", "% Change", "RS_55"]
            out_cols = ["Name", "LTP", "Change", "% Chg 20‑DMA", "RS_55"] if has_pct_20_dma else ["Name", "LTP", "Change", "RS_55"]

            top_etf = etf_df.nlargest(5, "RS_55")[cols].copy()
            top_etf.columns = out_cols
            html += _table_html(top_etf, out_cols, "Top 5 Leading ETFs", limit=5, zebra_color="#e6f4ea")

            bottom_etf = etf_df.nsmallest(5, "RS_55")[cols].copy()
            bottom_etf.columns = out_cols
            html += _table_html(bottom_etf, out_cols, "Bottom 5 Lagging ETFs", limit=5, zebra_color="#fbe9eb")

        html += _full_etf_table(etf_df)

    html += _etf_disclaimer()
    html += "</div>" + _html_foot()
    return html
