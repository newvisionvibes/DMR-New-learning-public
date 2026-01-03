"""
RS Value Interpretation Matrix & Usage Guide
Complete documentation for understanding Relative Strength values

RS-21: Short-term momentum (Intraday/Weekly trading)
RS-55: Medium-term momentum (Swing trading/2-4 weeks)
RS-123: Long-term momentum (Investment/2-3 months+)

Color coding:
Dark Green (>3%): Very Strong
Light Green (0-3%): Positive
Light Red (-1.5 to 0%): Weak
Dark Red (<-1.5%): Very Weak
"""

import streamlit as st
import pandas as pd  # kept for future data-based visuals


def build_readme_content() -> str:
    """Build comprehensive README content with all RS concepts and interpretations."""
    return """
# 📖 Sector RS Analyzer - Complete Guide

## 🎯 What is Relative Strength (RS)?

**Relative Strength** measures how well a sector is performing compared to a benchmark (usually NIFTY 50).

- **Positive RS** = Sector outperforming benchmark (bullish)
- **Negative RS** = Sector underperforming benchmark (bearish)
- **Higher RS** = Stronger momentum

---

## 📊 Three Time Periods Explained

### RS-21 (Short-term: 3 weeks)
**Use for:** Intraday & Weekly Trading
- Captures immediate momentum
- Sensitive to recent price moves
- Best for quick trading decisions
- Highly volatile

### RS-55 (Medium-term: 2-3 months)
**Use for:** Swing Trading (2-4 weeks)
- Balances short & long-term trends
- Most important indicator
- Best for trading decisions
- Most reliable

### RS-123 (Long-term: 6 months)
**Use for:** Investment Decisions
- Shows sustained strength
- Less affected by short-term noise
- Good for portfolio selection
- Confirms long-term trends

---

## 🎨 Color Coding Guide

### Green = Positive (Outperforming)
- **Dark Green (>3%)**: VERY STRONG - Leading market
- **Light Green (0-3%)**: Positive - Outperforming

### Red = Negative (Underperforming)
- **Light Red (-1.5% to 0%)**: Weak - Lagging benchmark
- **Dark Red (<-1.5%)**: VERY WEAK - Significantly behind

---

## 🔥 RS Value Interpretation Matrix

### All 27 Possible Combinations with Action Signals

---

## ✅ BEST COMBINATIONS (GO Signals)

### **1. 🚀 ALL GREEN (G-G-G)**
RS-21: +2.5%  |  RS-55: +4.0%  |  RS-123: +3.5%

**Signal:** ✅ STRONGEST BUY  
- Intraday: Perfect momentum for quick entry  
- Short-term (2-4 weeks): Ideal swing trade - all signals aligned  
- Mid-term (2-3 months): Excellent accumulation zone  
- Long-term: Strong portfolio holding  
- Action: All systems GO - Maximum confidence

---

### **2. 🎯 MEDIUM-LONG STRONG (R-G-G)**
RS-21: -1.0%  |  RS-55: +3.0%  |  RS-123: +2.5%

**Signal:** ✅ STRONG BUY - Consolidation Entry  
- Intraday: Short-term pullback, good buy opportunity  
- Short-term: Excellent entry with medium-long confirmation  
- Mid-term: Best risk-reward ratio  
- Long-term: Very good trending sector  
- Action: Preferred entry point - medium & long-term aligned

---

### **3. 💪 SHORT-MEDIUM STRONG (G-G-R)**
RS-21: +2.0%  |  RS-55: +3.5%  |  RS-123: -0.5%

**Signal:** ⚠️ BUY with Caution - Reversal Warning  
- Intraday: Strong short-term momentum  
- Short-term: Excellent trading opportunity  
- Mid-term: Best for 2–4 week swing trades  
- Long-term: Long-term trend weakening  
- Action: Tactical trades only, book profits early

---

### **4. 🎪 SHORT-MEDIUM PEAK (G-G-W)**
RS-21: +3.2%  |  RS-55: +2.8%  |  RS-123: -1.2%

**Signal:** ⚠️ PROFIT BOOKING - Avoid New Entry  
- Intraday: Move already extended  
- Short-term: Likely to face resistance  
- Mid-term: Reduce risk, lock gains  
- Long-term: Negative backdrop  
- Action: Exit or trim positions

---

## ⚠️ CAUTION COMBINATIONS (Sell/Avoid Signals)

### **5. 📉 ALL RED (R-R-R)**
RS-21: -2.0%  |  RS-55: -3.0%  |  RS-123: -2.5%

**Signal:** ❌ STRONGEST SELL - All Aligned Down  
- Intraday: Strong downtrend  
- Short-term: Persistent weakness  
- Mid-term: Clear negative trend  
- Long-term: Poor candidate for portfolios  
- Action: Exit / avoid

---

### **6. 🔴 SHORT-MEDIUM WEAK (R-R-G)**
RS-21: -2.5%  |  RS-55: -2.0%  |  RS-123: +1.5%

**Signal:** ❌ SELL - Medium-term Breakdown  
- Intraday: Selling pressure  
- Short-term: Weak participation  
- Mid-term: Breakdown despite long-term strength  
- Long-term: Not enough to fight medium-term trend  
- Action: Stand aside

---

### **7. 🏚️ MEDIUM-LONG WEAK (R-R-W)**
RS-21: -1.5%  |  RS-55: -1.8%  |  RS-123: -0.8%

**Signal:** ❌ AVOID - Broad Weakness  
- All horizons show lagging behaviour  
- Action: Observe only, do not deploy capital

---

### **8. 🚩 DETERIORATING (G-R-R)**
RS-21: +1.0%  |  RS-55: -2.0%  |  RS-123: -1.5%

**Signal:** ⚠️ SELL - Momentum Fading  
- Short-term strength appears inside a broader downtrend  
- Action: Use strength to exit rather than enter

---

## 🟡 MIXED / UNCERTAIN COMBINATIONS

(Examples like G-R-G, R-G-G, G-G-W, R-G-R, G-W-R, R-W-G – use them as practice cases to read RS behaviour.)

---

## 📈 Quick Decision Matrix by Time Horizon

### Intraday (minutes–hours)
- Focus on RS‑21
- Green: consider entries
- Deep red: avoid

### Short-term (2–4 weeks)
- Focus on RS‑55, confirm with RS‑21

### Mid-term (2–3 months)
- RS‑55 primary, RS‑123 confirmation

### Long-term (6+ months)
- RS‑123 primary, RS‑55 confirmation

---

## 🎓 Best Practices

- Let RS‑55 be the “teacher”; RS‑21 and RS‑123 are supporting signals.
- Avoid trades when all three are clearly red.
- Treat this guide as an educational checklist, not a trading recommendation.

---

## ❓ FAQ (Learner Focused)

- Can I use only RS‑21?  
  Better to combine with RS‑55 to reduce noise.

- What if only RS‑55 is green?  
  Often suitable for swing‑trading style learning.

- How often should RS be checked?  
  Daily for active learning, weekly for swing view, monthly for long‑term view.

**Happy Learning! Align with RS‑55 and confirm with the others.** 📊🚀
"""


def render_full_rs_readme() -> None:
    """Full RS guide for admin / deep learners."""
    st.markdown(build_readme_content())


def render_rs_concepts_for_students() -> None:
    """
    Focused RS concepts view for subscribers.
    Same educational tone, optimised for a dedicated tab.
    """
    st.markdown("## 📊 RS Power Lab – Understanding Relative Strength")
    st.caption(
        "Use this section to study RS‑21, RS‑55, and RS‑123 and how colour signals change across timeframes."
    )
    st.markdown(build_readme_content())


def render_readme_tab() -> None:
    """
    Render the Learning Guide tab, including the interactive RS matrix.
    Suitable as the main educational README for subscribers.
    """
    render_rs_concepts_for_students()

    st.divider()
    st.subheader("🎯 Interactive RS Matrix Selector")
    st.caption("Choose RS colours to see a learning‑friendly interpretation for each timeframe.")

    col1, col2, col3 = st.columns(3)

    with col1:
        rs21_color = st.selectbox(
            "RS-21 (Short-term)",
            ["🔴 Red", "🟡 Neutral", "🟢 Green"],
            key="rs21_select",
        )
    with col2:
        rs55_color = st.selectbox(
            "RS-55 (Medium-term)",
            ["🔴 Red", "🟡 Neutral", "🟢 Green"],
            key="rs55_select",
        )
    with col3:
        rs123_color = st.selectbox(
            "RS-123 (Long-term)",
            ["🔴 Red", "🟡 Neutral", "🟢 Green"],
            key="rs123_select",
        )

    color_map = {"🔴 Red": "Red", "🟡 Neutral": "Neutral", "🟢 Green": "Green"}
    rs21 = color_map[rs21_color]
    rs55 = color_map[rs55_color]
    rs123 = color_map[rs123_color]

    combination = f"{rs21}-{rs55}-{rs123}"

    interpretations = {
        "Green-Green-Green": {
            "signal": "✅ STRONGEST BUY - All Aligned",
            "intraday": "Strong intraday momentum, suitable for active trades.",
            "short_term": "Very good swing‑trade setup with all periods positive.",
            "mid_term": "Favourable zone for gradual accumulation.",
            "long_term": "Healthy candidate for long‑term holding.",
            "confidence": "⭐⭐⭐⭐⭐",
        },
        "Red-Red-Red": {
            "signal": "❌ STRONGEST SELL - All Aligned Down",
            "intraday": "Downtrend dominates; avoid fresh long positions.",
            "short_term": "Consistent weakness vs benchmark.",
            "mid_term": "Downtrend in progress; learning focus only.",
            "long_term": "Unfavourable for long‑term portfolios.",
            "confidence": "⭐⭐⭐⭐⭐",
        },
        "Green-Green-Red": {
            "signal": "⚠️ BUY WITH CAUTION - Reversal Warning",
            "intraday": "Short‑term strength visible.",
            "short_term": "Good trading window for 2–4 weeks.",
            "mid_term": "Useful for tactical positions.",
            "long_term": "Long‑term trend soft; monitor closely.",
            "confidence": "⭐⭐⭐⭐",
        },
        "Red-Green-Green": {
            "signal": "💡 BUY ON DIPS - Reversal Forming",
            "intraday": "Minor pullback inside a broader uptrend.",
            "short_term": "Improving structure; dips can be used for practice entries.",
            "mid_term": "Positive recovery in progress.",
            "long_term": "Supportive backdrop for investors.",
            "confidence": "⭐⭐⭐⭐⭐",
        },
        "Green-Red-Red": {
            "signal": "⚠️ SELL - Momentum Fading",
            "intraday": "Bounce on a weak background.",
            "short_term": "Strength not sustaining beyond very short term.",
            "mid_term": "Clear sign of deterioration.",
            "long_term": "Downtrend; better to observe than participate.",
            "confidence": "⭐⭐⭐⭐",
        },
        "Red-Red-Green": {
            "signal": "❌ SELL - Medium-term Breakdown",
            "intraday": "Selling pressure dominates.",
            "short_term": "Medium‑term trend under strain.",
            "mid_term": "Breakdown despite long‑term support.",
            "long_term": "Only the longest frame is positive; not sufficient alone.",
            "confidence": "⭐⭐⭐",
        },
    }

    interp = interpretations.get(combination)

    if interp:
        st.success(f"**{interp['signal']}**")
        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### ⏰ View by Time Horizon")
            st.write(f"🕐 **Intraday:** {interp['intraday']}")
            st.write(f"📅 **Short-term (2–4 weeks):** {interp['short_term']}")
            st.write(f"📊 **Mid-term (2–3 months):** {interp['mid_term']}")
            st.write(f"📈 **Long-term (6+ months):** {interp['long_term']}")

        with c2:
            st.markdown("### 📊 Confidence Level")
            st.write(f"**Signal Strength:** {interp['confidence']}")

            if "STRONGEST" in interp["signal"]:
                st.warning("⚠️ Perfect alignment – highest confidence pattern for study.")
            elif "CAUTION" in interp["signal"] or "WARNING" in interp["signal"]:
                st.info("ℹ️ Mixed timeframes – treat this as an advanced learning setup.")
            elif "SELL" in interp["signal"]:
                st.error("🔴 Downside risk is high – focus on understanding, not trading.")
            else:
                st.success("✅ Constructive pattern – good case study for practice.")
    else:
        st.info("ℹ️ Select a combination of RS colours to see an interpretation matrix.")


if __name__ == "__main__":
    render_readme_tab()
