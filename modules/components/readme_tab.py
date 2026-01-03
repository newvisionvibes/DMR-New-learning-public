"""
README TAB - EDUCATIONAL CONTENT
For subscribers to learn about the platform
File: pages/readme_tab.py (or add to main.py as a tab)
"""

import streamlit as st


def render_readme_tab():
    """
    Educational README tab for subscribers
    Provides learning-focused content about the platform
    """
    
    st.markdown("# 📚 Learning Guide - Understanding Market Analysis")
    st.divider()
    
    # Introduction Section
    with st.container():
        st.markdown("## 🎓 Welcome to Your Learning Platform")
        st.markdown("""
        This platform is designed to help you **learn market analysis** by analyzing real NSE market data. 
        Think of it as your personal classroom for understanding how sectors and ETFs behave in the market!
        """)
    
    st.divider()
    
    # Tabs for organized content
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 Getting Started", 
        "📊 Understanding RS", 
        "🏢 Sectors", 
        "💼 ETFs", 
        "💡 Tips & Resources"
    ])
    
    # TAB 1: Getting Started
    with tab1:
        st.markdown("### 📖 Getting Started with This Platform")
        
        st.markdown("#### What Will You Learn?")
        st.markdown("""
        This educational platform teaches you:
        
        1. **Relative Strength (RS) Analysis** - How to identify strong vs weak performers
        2. **Sector Analysis** - Understanding which sectors are performing well
        3. **ETF Analysis** - Learning about Exchange-Traded Funds and their behavior
        4. **Market Intelligence** - Reading real market data to make informed decisions
        """)
        
        st.markdown("#### How to Use This Platform")
        st.markdown("""
        **Step 1:** Go to **Sector Analysis Report**
        - View how 19 NSE sectors are performing
        - See which sectors are outperforming the market
        
        **Step 2:** Go to **ETF Analysis Report**
        - Analyze 100+ ETFs across different categories
        - Track their relative strength movements
        
        **Step 3:** Go to **Comprehensive Report**
        - See a complete analysis combining sectors and ETFs
        - Understand the broader market picture
        """)
        
        st.success("✨ **Tip:** Start with Sector Analysis to understand the basics!")
    
    # TAB 2: Understanding Relative Strength
    with tab2:
        st.markdown("### 📊 What is Relative Strength (RS)?")
        
        st.markdown("#### Simple Definition")
        st.markdown("""
        **Relative Strength** is a way to compare how one stock/sector is doing compared to a benchmark 
        (like NIFTY 50).
        
        Think of it like this:
        - If NIFTY 50 goes up 10%, and your sector goes up 15%, then your sector has **strong** relative strength
        - If NIFTY 50 goes up 10%, and your sector goes up 5%, then your sector has **weak** relative strength
        """)
        
        st.markdown("#### Why RS Matters for Learning")
        st.markdown("""
        RS helps you understand:
        - ✅ Which sectors are market leaders
        - ✅ Which sectors are lagging behind
        - ✅ Where money is flowing in the market
        - ✅ Which ETFs are performing best
        """)
        
        st.markdown("#### RS-55 Indicator")
        st.markdown("""
        **RS-55** is a specific metric we use:
        - Compares 55-day performance vs benchmark
        - Positive RS-55 = Strong performance
        - Negative RS-55 = Weak performance
        - Values closer to 0 = Similar to benchmark
        
        **Example:**
        - Bank sector RS-55 = +9.5% → Banks are doing better than market average
        - Auto sector RS-55 = -2.3% → Auto is doing worse than market average
        """)
        
        st.info("💡 **Learning Point:** Use RS to spot which sectors are hot and which are cold!")
    
    # TAB 3: Understanding Sectors
    with tab3:
        st.markdown("### 🏢 What Are Sectors?")
        
        st.markdown("#### Definition")
        st.markdown("""
        A **sector** is a group of companies in the same industry. The NSE groups companies into 19 main sectors.
        """)
        
        st.markdown("#### Examples of Major Sectors")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Financial Services**
            - Banks, Insurance companies
            - Stock brokers, Financial services
            
            **Energy**
            - Oil & Gas companies
            - Power generation
            
            **Metals & Mining**
            - Metals companies
            - Mining companies
            
            **Auto**
            - Car manufacturers
            - Auto component makers
            """)
        
        with col2:
            st.markdown("""
            **Information Technology**
            - Software companies
            - IT Services
            
            **Pharma**
            - Medicine manufacturers
            - Healthcare companies
            
            **Consumer**
            - FMCG (daily use items)
            - Retail companies
            
            **Utilities**
            - Power distribution
            - Water supply companies
            """)
        
        st.markdown("#### Why Learn About Sectors?")
        st.markdown("""
        - 📈 Different sectors perform differently at different times
        - 🎯 Understanding sector trends helps you spot opportunities
        - 💰 Some sectors do well in good economy, others in bad economy
        - 🔍 Sector analysis is the foundation of market analysis
        """)
        
        st.warning("📌 **Remember:** Markets are not all the same - sectors vary significantly!")
    
    # TAB 4: Understanding ETFs
    with tab4:
        st.markdown("### 💼 What Are ETFs?")
        
        st.markdown("#### Simple Definition")
        st.markdown("""
        An **ETF** (Exchange-Traded Fund) is like a basket of stocks that you can buy and sell easily,
        just like buying a single stock.
        
        **Analogy:** Think of an ETF like a food basket:
        - Instead of buying individual vegetables from different shops
        - You buy a pre-made basket with a mix of vegetables
        - You get variety with one purchase
        """)
        
        st.markdown("#### Types of ETFs (You'll See in Analysis)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Index ETFs**
            - Track NIFTY 50
            - Track Bank Nifty
            - Track Sensex
            
            **Sector ETFs**
            - Bank ETFs
            - IT ETFs
            - Pharma ETFs
            """)
        
        with col2:
            st.markdown("""
            **Thematic ETFs**
            - Infrastructure ETFs
            - Energy ETFs
            - Gold ETFs
            
            **International ETFs**
            - US market ETFs
            - Emerging market ETFs
            """)
        
        st.markdown("#### Why ETFs Are Great for Learning")
        st.markdown("""
        - 🎓 Easy way to track whole sectors or themes
        - 💡 Simpler than analyzing 50+ individual stocks
        - 📊 Real price movements you can analyze
        - 🔄 Shows sector trends clearly
        """)
        
        st.success("✨ **Insight:** If a sector ETF is rising, it means that whole sector is doing well!")
    
    # TAB 5: Tips & Resources
    with tab5:
        st.markdown("### 💡 Learning Tips & Best Practices")
        
        st.markdown("#### How to Read the Reports")
        st.markdown("""
        1. **Look at Rankings** - Which sectors/ETFs are at top (strongest)?
        2. **Check RS Values** - Are they positive (strong) or negative (weak)?
        3. **Compare Over Time** - Are things improving or getting worse?
        4. **Find Patterns** - Do certain sectors move together?
        """)
        
        st.markdown("#### Common Learner Questions")
        
        with st.expander("❓ Why does RS change so frequently?"):
            st.markdown("""
            RS changes because:
            - Stock prices change every minute
            - Benchmark (NIFTY 50) also changes
            - RS = relative comparison, so both matter
            
            **Learning Point:** Markets are dynamic - this teaches you about continuous change!
            """)
        
        with st.expander("❓ Why are some sectors always weak?"):
            st.markdown("""
            Some sectors are weak because:
            - They face industry challenges (e.g., auto waiting for new tech)
            - Economic conditions don't favor them
            - Investor interest shifts to other sectors
            
            **Learning Point:** All sectors have seasons - some hot, some cold!
            """)
        
        with st.expander("❓ How to predict which sector will be strong?"):
            st.markdown("""
            This requires:
            - Understanding economic cycles
            - Following market news
            - Analyzing historical patterns
            - Learning technical analysis
            
            **Learning Point:** Prediction is an art learned over time!
            """)
        
        st.markdown("#### Resources for Further Learning")
        st.markdown("""
        **Learn About Markets:**
        - NSE India Official Website
        - Investopedia - Market Basics
        - Moneycontrol - Daily Analysis
        
        **Learn Technical Analysis:**
        - Relative Strength concept
        - Chart patterns
        - Trend analysis
        
        **Practice Your Skills:**
        - Track sectors weekly
        - Note which patterns repeat
        - Keep a learning journal
        """)
        
        st.markdown("#### Study Ideas")
        st.markdown("""
        1. **Weekly Analysis Habit**
           - Check the reports every Friday
           - Note top 3 performing sectors
           - Note bottom 3 performing sectors
           - Try to understand why
        
        2. **Comparison Exercise**
           - Compare this week to last week
           - Which sectors improved?
           - Which sectors got worse?
           - What news explains these moves?
        
        3. **Sector Diary**
           - Keep notes on each sector
           - Record when it's strong/weak
           - Note major news affecting it
           - Track your predictions
        """)
        
        st.success("🎓 **Remember:** Consistent learning beats sporadic study!")
    
    st.divider()
    
    # Final Section
    with st.container():
        st.markdown("## 🎯 Your Learning Journey")
        
        st.markdown("""
        ### Stage 1: Understand the Basics (Week 1-2)
        - Learn what sectors and ETFs are
        - Understand what Relative Strength means
        - Read the reports regularly
        
        ### Stage 2: Start Analyzing (Week 3-4)
        - Compare week-on-week changes
        - Identify sector trends
        - Start making observations
        
        ### Stage 3: Deep Dive (Week 5-8)
        - Correlate sectors with news
        - Understand sector relationships
        - Predict likely movers
        
        ### Stage 4: Advanced Learning (Month 3+)
        - Learn technical analysis
        - Combine with fundamental analysis
        - Develop your analysis style
        """)
        
        st.info("""
        💡 **Pro Tip:** The best way to learn is by doing. 
        Keep updating your analysis notes every week and review them monthly!
        """)
    
    st.divider()
    
    # Contact/Support Section
    st.markdown("## 📞 Need Help?")
    st.markdown("""
    **Questions About Market Analysis?**
    - Review this Learning Guide
    - Check the report explanations
    - Look for patterns in historical data
    
    **Have Feedback?**
    - Your feedback helps improve this platform
    - Let us know what you'd like to learn more about
    
    **Remember:** Every expert analyst was once a beginner!
    """)
    
    st.success("""
    ✨ **Happy Learning!** 
    Take your time, practice regularly, and watch your market analysis skills grow! 🚀
    """)


# If this is run as main, render the tab
if __name__ == "__main__":
    render_readme_tab()
