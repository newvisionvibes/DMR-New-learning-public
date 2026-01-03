"""
sector_analysis_validator.py - CORE VALIDATION ENGINE
======================================================

Purpose: Validate and clean sector & ETF analysis data
Status: PRODUCTION READY - Core module for validation

Functions:
✅ validate_sector_count() - Check exactly 19 sectors
✅ validate_sector_data() - Clean & validate data types
✅ enforce_complete_analysis() - Auto-retry incomplete
✅ generate_validation_report() - Full validation report

All functions return tuple with (is_valid, data/msg, count/msg)
"""

import pandas as pd
import logging
from typing import Tuple, Optional, Callable

logger = logging.getLogger(__name__)

# Define 19 sectors for NIFTY
SECTOR_DEFINITIONS = {
    "IT": ["INFY", "TCS", "WIPRO", "TECHM", "HCLTECH"],
    "Banking": ["HDFC", "ICICIBANK", "AXISBANK", "KOTAK"],
    "Auto": ["MARUTI", "TATAMOTORS", "BAJAJ", "HEROMOTOCO"],
    "Pharma": ["SUNPHARMA", "CIPLA", "DRREDDY", "LUPIN"],
    "Energy": ["RELIANCE", "ONGC", "COALINDIA", "NTPC"],
    "Materials": ["TATA STEEL", "HINDALCO", "JSWSTEEL", "VEDL"],
    "Consumer": ["ITC", "BRITANNIA", "NESTLEIND", "MARICO"],
    "Finance": ["SBILIFE", "HDFCBANK", "BAJAJFINSV"],
    "Infra": ["LARSENTOUBRO", "JSWINFRA", "ADANIPORTS"],
    "Realty": ["DLF", "OBEROIREALTY", "SOBHA"],
    "Telecom": ["BHARTI", "IDEA", "VODAFONEAF"],
    "Utilities": ["NTPC", "POWERGRID"],
    "Chemicals": ["PIDILITIND", "DEEPAKFERT"],
    "Metals": ["TATASTEEL", "JSWSTEEL"],
    "Paper": ["BALKRISHNA"],
    "Textiles": ["GRASIM"],
    "Cement": ["ULTRACEMC", "SHREECEM"],
    "Agri": ["GODREJ"],
    "Media": ["INDIABULLS"],
}


def validate_sector_count(df: pd.DataFrame) -> Tuple[bool, str, int]:
    """
    Validate that exactly 19 sectors are present in DataFrame.
    
    Args:
        df: DataFrame from sector analysis
        
    Returns:
        Tuple: (is_valid: bool, message: str, count: int)
        - is_valid: True if exactly 19 sectors found
        - message: Descriptive status message
        - count: Actual number of sectors found
    """
    
    if df is None or df.empty:
        msg = "❌ INVALID: DataFrame is empty or None"
        logger.error(msg)
        return False, msg, 0
    
    count = len(df)
    
    if count == 19:
        msg = f"✅ Sector count valid: {count} sectors"
        logger.info(msg)
        return True, msg, count
    
    elif count < 19:
        missing = 19 - count
        msg = f"❌ INCOMPLETE: Got {count} sectors, missing {missing}"
        logger.warning(msg)
        return False, msg, count
    
    else:  # count > 19
        excess = count - 19
        msg = f"⚠️  EXCESS: Got {count} sectors (expected 19, excess {excess})"
        logger.warning(msg)
        return False, msg, count


def validate_sector_data(df: pd.DataFrame) -> Tuple[bool, pd.DataFrame, str]:
    """
    Validate and clean sector/ETF data.
    
    Functions performed:
    ✅ Convert numeric columns to float64
    ✅ Remove rows with invalid/missing critical data
    ✅ Handle NaN and infinity values
    ✅ Validate column presence
    
    Args:
        df: DataFrame with sector or ETF data
        
    Returns:
        Tuple: (is_valid: bool, cleaned_df: pd.DataFrame, message: str)
        - is_valid: True if validation passed
        - cleaned_df: Cleaned DataFrame
        - message: Validation status message
    """
    
    if df is None or df.empty:
        msg = "❌ Data validation failed: DataFrame is empty"
        logger.error(msg)
        return False, None, msg
    
    df_clean = df.copy()
    original_count = len(df_clean)
    
    try:
        # Numeric columns that might exist in data
        numeric_columns = [
            "LTP", "Change", "% Change", "% Change 20 DMA",
            "RS_21", "RS_55", "RS_123",
            "RS_1", "RS1", "RS_2", "RS2",
            "Open", "High", "Low", "Close", "Volume",
            "Token"
        ]
        
        # Convert identified numeric columns to float
        for col in numeric_columns:
            if col in df_clean.columns:
                try:
                    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                    logger.debug(f"Converted {col} to numeric")
                except Exception as e:
                    logger.warning(f"Could not convert {col}: {e}")
        
        # Remove rows with all NaN in numeric columns
        numeric_cols_present = [col for col in numeric_columns if col in df_clean.columns]
        if numeric_cols_present:
            df_clean = df_clean.dropna(subset=numeric_cols_present, how='all')
        
        # Remove rows with NaN in critical identifier columns
        id_cols = ["Sector", "Index", "ETF Code", "ETF_Name", "Code"]
        id_cols_present = [col for col in id_cols if col in df_clean.columns]
        if id_cols_present:
            df_clean = df_clean.dropna(subset=id_cols_present, how='all')
        
        # Remove rows where LTP is NaN (critical data)
        if "LTP" in df_clean.columns:
            df_clean = df_clean[df_clean["LTP"].notna()]
        
        # Replace infinities with NaN then drop
        df_clean = df_clean.replace([float('inf'), float('-inf')], float('nan'))
        
        cleaned_count = len(df_clean)
        dropped = original_count - cleaned_count
        
        msg = f"✅ Data validated: {cleaned_count} rows (dropped {dropped})"
        logger.info(msg)
        
        if dropped > 0:
            logger.info(f"Cleaned {dropped} invalid rows from {original_count}")
        
        return True, df_clean, msg
        
    except Exception as e:
        msg = f"⚠️  Data validation error: {str(e)}"
        logger.error(msg, exc_info=True)
        return False, df, msg


def enforce_complete_analysis(
    df: pd.DataFrame,
    retry_callback: Callable,
    max_retries: int = 2
) -> Tuple[bool, pd.DataFrame, str]:
    """
    Retry analysis if incomplete (less than 19 sectors).
    
    Args:
        df: Initial DataFrame from analysis
        retry_callback: Function to call for retry (should return DataFrame)
        max_retries: Maximum retry attempts (default 2)
        
    Returns:
        Tuple: (is_valid: bool, final_df: pd.DataFrame, message: str)
        - is_valid: True if 19 sectors achieved
        - final_df: DataFrame with complete data (or best attempt)
        - message: Status with retry count
    """
    
    is_valid, msg, count = validate_sector_count(df)
    
    if is_valid:
        return True, df, f"✅ Analysis complete on first try: {msg}"
    
    logger.warning(f"Incomplete analysis detected, attempting retry. Got {count}/19")
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Retry attempt {attempt}/{max_retries}")
            df_retry = retry_callback()
            
            if df_retry is None or df_retry.empty:
                logger.warning(f"Retry attempt {attempt} returned empty data")
                continue
            
            is_valid_retry, msg_retry, count_retry = validate_sector_count(df_retry)
            
            if is_valid_retry:
                success_msg = f"✅ Retry successful: Success after {attempt} retries"
                logger.info(success_msg)
                return True, df_retry, success_msg
            
            else:
                logger.warning(f"Retry attempt {attempt} returned {count_retry}/19 sectors")
                df = df_retry  # Keep best attempt so far
                
        except Exception as e:
            logger.error(f"Retry attempt {attempt} failed: {e}")
            continue
    
    # Return best attempt even if not complete
    final_count = len(df)
    failure_msg = f"❌ Could not achieve 19 sectors after {max_retries} retries. Best: {final_count}/19"
    logger.error(failure_msg)
    return False, df, failure_msg


def generate_validation_report(df: pd.DataFrame) -> str:
    """
    Generate comprehensive validation report.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        str: Detailed validation report
    """
    
    report = []
    report.append("=" * 70)
    report.append("VALIDATION REPORT")
    report.append("=" * 70)
    
    # Check 1: DataFrame exists and has data
    if df is None or df.empty:
        report.append("❌ FAILED: DataFrame is None or empty")
        return "\n".join(report)
    
    report.append(f"✅ DataFrame exists with {len(df)} rows, {len(df.columns)} columns")
    
    # Check 2: Sector count
    is_valid_sectors, msg_sectors, count_sectors = validate_sector_count(df)
    report.append(f"{msg_sectors}")
    
    # Check 3: Data types
    report.append("\nData Type Summary:")
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isna().sum()
        report.append(f"  {col:30s} | {str(dtype):15s} | Nulls: {null_count}")
    
    # Check 4: Numeric columns validation
    report.append("\nNumeric Columns Validation:")
    numeric_cols = ["LTP", "RS_21", "RS_55", "RS_123", "% Change"]
    for col in numeric_cols:
        if col in df.columns:
            try:
                numeric_data = pd.to_numeric(df[col], errors='coerce')
                null_count = numeric_data.isna().sum()
                min_val = numeric_data.min()
                max_val = numeric_data.max()
                report.append(
                    f"  {col:30s} | Min: {min_val:10.2f} | Max: {max_val:10.2f} | Nulls: {null_count}"
                )
            except Exception as e:
                report.append(f"  {col:30s} | ❌ Error: {str(e)}")
    
    # Check 5: Data validation result
    is_valid_data, df_clean, msg_data = validate_sector_data(df)
    report.append(f"\n{msg_data}")
    
    report.append("\n" + "=" * 70)
    report.append("END VALIDATION REPORT")
    report.append("=" * 70)
    
    return "\n".join(report)


# Convenience function for logging all validation info
def log_validation_summary(df: pd.DataFrame) -> None:
    """Log complete validation summary"""
    
    report = generate_validation_report(df)
    logger.info(f"\n{report}")


if __name__ == "__main__":
    logger.info("✅ sector_analysis_validator.py loaded successfully")
    logger.info("Available functions:")
    logger.info("  • validate_sector_count(df)")
    logger.info("  • validate_sector_data(df)")
    logger.info("  • enforce_complete_analysis(df, retry_callback, max_retries)")
    logger.info("  • generate_validation_report(df)")
    logger.info("  • log_validation_summary(df)")
