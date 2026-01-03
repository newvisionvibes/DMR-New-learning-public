"""
Enhanced ETF RS Calculator V2 - CIRCULAR IMPORT FIXED

Calculates: LTP, % Change, 20-DMA, % Change 20 DMA, RS-21/55/123, TLDR

Features:
- Fetch 400 days of historical data per ETF
- Calculate 20-day moving average
- Compute daily % change from previous close
- Compute % change from 20-DMA
- Calculate RS vs NIFTY 50 benchmark
- Generate TLDR summary for each ETF
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

BENCHMARK_TOKEN = "99926000"  # NIFTY 50 index token
BENCHMARK_EXCHANGE = "NSE"


def get_candles(smartapi, token, days_back=400, exchange="NSE"):
    """Fetch daily candles for given token with rate limit protection."""
    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_back)
    
    params = {
        "exchange": exchange,
        "symboltoken": str(token),
        "interval": "ONE_DAY",
        "fromdate": from_date.strftime("%Y-%m-%d 09:15"),
        "todate": to_date.strftime("%Y-%m-%d 15:30"),
    }
    
    retries = 3
    for attempt in range(retries):
        try:
            data = smartapi.getCandleData(params)
            
            # Check for rate limit error
            if isinstance(data, str) and "exceeding access rate" in data.lower():
                print(f"⚠️ Rate limit hit for token {token}, using cached fallback")
                return None
            
            if not data or not data.get("status") or not data.get("data"):
                return None
            
            df = pd.DataFrame(
                data["data"],
                columns=["timestamp", "open", "high", "low", "close", "volume"],
            )
            
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["close"] = df["close"].astype(float)
            
            return df.sort_values("timestamp").reset_index(drop=True)
        
        except Exception as e:
            error_msg = str(e).lower()
            
            # Rate limit: stop immediately, don't retry
            if "exceeding access rate" in error_msg:
                print(f"⚠️ Rate limit hit for token {token}, no retry")
                return None
            
            # Server error: wait and retry
            if "something went wrong" in error_msg or "ab1004" in error_msg:
                if attempt < retries - 1:
                    wait_time = 60 + (attempt * 30)
                    print(f"⚠️ Server error, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    continue
            
            print(f"⚠️ Error fetching candles for token {token}: {str(e)[:80]}")
            return None
    
    return None


def compute_rs(etf_df, bm_df, period):
    """Compute RS over given period in days."""
    if etf_df is None or bm_df is None:
        return None
    
    if len(etf_df) <= period or len(bm_df) <= period:
        return None
    
    merged = pd.merge(
        etf_df[["timestamp", "close"]].rename(columns={"close": "etf_close"}),
        bm_df[["timestamp", "close"]].rename(columns={"close": "bm_close"}),
        on="timestamp",
        how="inner",
    )
    
    if len(merged) <= period:
        return None
    
    etf_ret = (merged["etf_close"].iloc[-1] / merged["etf_close"].iloc[-period] - 1) * 100
    bm_ret = (merged["bm_close"].iloc[-1] / merged["bm_close"].iloc[-period] - 1) * 100
    
    return round(etf_ret - bm_ret, 2)


def calculate_20_dma(df):
    """Calculate 20-day moving average."""
    if df is None or len(df) < 20:
        return None
    return round(df["close"].tail(20).mean(), 2)


def calculate_pct_change_from_20dma(df):
    """Calculate % change from 20-DMA."""
    if df is None or len(df) < 20:
        return None
    
    dma_20 = df["close"].tail(20).mean()
    current_price = df["close"].iloc[-1]
    pct_change = (current_price - dma_20) / dma_20 * 100
    
    return round(pct_change, 2)


def get_etf_tldr(rs21: float, rs55: float, rs123: float, pct_change: float) -> str:
    """Generate TLDR for ETFs based on RS and price action."""
    rs21 = rs21 or 0.0
    rs55 = rs55 or 0.0
    rs123 = rs123 or 0.0
    pct_change = pct_change or 0.0
    
    if rs55 >= 3 and rs21 > 0 and rs123 > 0:
        return "Very strong momentum - Multi-timeframe leader"
    
    if rs55 >= 1.5 and rs21 > 0:
        return "Strong uptrend - Buy on dips"
    
    if rs55 <= -3:
        return "Severe underperformance - Avoid for now"
    
    if rs55 <= -1.5 and rs21 < 0:
        return "Weak trend - Lagging benchmark"
    
    if pct_change > 1 and rs21 > 0:
        return "Short-term surge - Watch follow-through"
    
    if pct_change < -1 and rs21 < 0:
        return "Short-term pressure - Avoid fresh entries"
    
    return "Sideways / volatile - Wait for clear trend"


def load_cached_etf_data(etf_name):
    """Load cached data from CSV if fresh data unavailable."""
    try:
        cached_df = pd.read_csv("etf_rs_output.csv")
        cached_row = cached_df[cached_df['Ticker'] == etf_name]
        
        if not cached_row.empty:
            return {
                'LTP': cached_row.iloc[0].get('LTP', 0),
                'Change': cached_row.iloc[0].get('Change', 0),
                'RS_21': cached_row.iloc[0].get('RS_21', '-'),
                'RS_55': cached_row.iloc[0].get('RS_55', '-'),
                'RS_123': cached_row.iloc[0].get('RS_123', '-'),
                'TLDR': 'Using cached data'
            }
    except Exception as e:
        print(f"Cache lookup failed for {etf_name}: {e}")
    
    return None


def calculate_etf_rs(smartapi, etf_csv_path, periods=(21, 55, 123)):
    """
    Read ETFs-List_updated.csv and compute complete metrics for each ETF.
    
    Returns DataFrame with columns:
    - ETF Code
    - Sector/Theme
    - LTP (Latest Trading Price)
    - % Change (vs Previous Close)
    - 20 DMA (20-Day Moving Average)
    - % Change 20 DMA (Price vs 20-DMA)
    - RS_21, RS_55, RS_123
    - TLDR (narrative summary)
    """
    
    try:
        etf_list = pd.read_csv(etf_csv_path)
    except Exception as e:
        print(f"❌ Failed to load ETF list: {e}")
        return None
    
    # Get benchmark data
    print("Fetching benchmark (NIFTY 50) data...")
    bm_df = get_candles(
        smartapi,
        BENCHMARK_TOKEN,
        days_back=400,
        exchange=BENCHMARK_EXCHANGE,
    )
    
    if bm_df is None:
        print("⚠️ Benchmark data unavailable, using fallback")
        bm_df = pd.DataFrame()  # Empty fallback
    
    results = []
    failed_count = 0
    
    for idx, row in etf_list.iterrows():
        etf_code = row.get("ETF Code", f"ETF_{idx}")
        token = row.get("Token") or row.get("token") or row.get("numeric_token")
        sector = row.get("Sector/Theme", "Unknown")
        
        print(f"[{idx+1}/{len(etf_list)}] Processing {etf_code}...")
        
        try:
            # Try to get fresh data
            etf_df = get_candles(smartapi, token, days_back=400, exchange="NSE")
            
            # Handle no data (API rate limit or unavailable)
            if etf_df is None or len(etf_df) == 0:
                print(f"   ⚠️ No fresh data for {etf_code}, checking cache...")
                
                cached = load_cached_etf_data(etf_code)
                if cached:
                    results.append({
                        "ETF Code": etf_code,
                        "Sector/Theme": sector,
                        "LTP": cached['LTP'],
                        "% Change": cached['Change'],
                        "% Change 20 DMA": '-',
                        "20 DMA": '-',
                        "RS_21": cached['RS_21'],
                        "RS_55": cached['RS_55'],
                        "RS_123": cached['RS_123'],
                        "TLDR": cached['TLDR'],
                    })
                    print(f"   ✅ Using cached data")
                    continue
                
                failed_count += 1
                print(f"   ⏭️ Skipping (no data, no cache)")
                continue
            
            # Validate data
            if 'close' not in etf_df.columns or len(etf_df) == 0:
                print(f"   ⚠️ Invalid data structure")
                failed_count += 1
                continue
            
            # Calculate metrics
            if bm_df is not None and len(bm_df) > 0:
                rs_21 = compute_rs(etf_df, bm_df, 21)
                rs_55 = compute_rs(etf_df, bm_df, 55)
                rs_123 = compute_rs(etf_df, bm_df, 123)
            else:
                rs_21 = rs_55 = rs_123 = None
            
            ltp = round(etf_df["close"].iloc[-1], 2)
            
            prev_close = etf_df["close"].iloc[-2] if len(etf_df) > 1 else etf_df["close"].iloc[-1]
            pct_change = round(((ltp - prev_close) / prev_close * 100) if prev_close != 0 else 0, 2)
            
            dma_20 = calculate_20_dma(etf_df)
            pct_change_20dma = calculate_pct_change_from_20dma(etf_df)
            
            tldr = get_etf_tldr(
                rs_21 if rs_21 is not None else 0.0,
                rs_55 if rs_55 is not None else 0.0,
                rs_123 if rs_123 is not None else 0.0,
                pct_change if pct_change is not None else 0.0,
            )
            
            results.append({
                "ETF Code": etf_code,
                "Sector/Theme": sector,
                "LTP": ltp,
                "% Change": pct_change,
                "% Change 20 DMA": pct_change_20dma,
                "20 DMA": dma_20,
                "RS_21": round(rs_21, 2) if rs_21 is not None else "-",
                "RS_55": round(rs_55, 2) if rs_55 is not None else "-",
                "RS_123": round(rs_123, 2) if rs_123 is not None else "-",
                "TLDR": tldr,
            })
            
            print(f"   ✅ RS: {rs_21}/{rs_55}/{rs_123}")
        
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:80]}")
            failed_count += 1
            continue
        
        # Rate limit protection
        time.sleep(0.5)
    
    if not results:
        print("\n⚠️ No ETF data obtained")
        return None
    
    df_result = pd.DataFrame(results)
    print(f"\n✅ Processed: {len(results)} ETFs")
    print(f"⚠️ Failed: {failed_count} ETFs")
    
    return df_result
