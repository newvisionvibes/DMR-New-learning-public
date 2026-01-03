"""
UPDATED: data_refresh_tracker.py (v3)
Fixes double "IST IST" suffix issue

Changes from v2:
1. ✅ Fixed: Double IST suffix removal
2. ✅ Fixed: IST timezone in datetime parsing
3. ✅ Uses IST for all operations
4. ✅ No duplicate "IST" in output
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import pytz

TRACKER_FILE = "refresh_tracker.json"
IST = pytz.timezone("Asia/Kolkata")


class DataRefreshTracker:
    """
    Tracks refresh times for sectors, ETFs, and combined data.
    Uses JSON file as primary storage (no database dependency).
    """
    
    @staticmethod
    def _ensure_file_exists():
        """Create refresh_tracker.json if it doesn't exist."""
        if not os.path.exists(TRACKER_FILE):
            default_data = {
                "sectors": {
                    "last_refresh": "Never",
                    "status": "unknown",
                    "count": 0,
                    "freshness": "unknown"
                },
                "etfs": {
                    "last_refresh": "Never",
                    "status": "unknown",
                    "count": 0,
                    "freshness": "unknown"
                },
                "comprehensive": {
                    "last_refresh": "Never",
                    "status": "unknown",
                    "count": 0,
                    "freshness": "unknown"
                }
            }
            try:
                with open(TRACKER_FILE, "w") as f:
                    json.dump(default_data, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not create {TRACKER_FILE}: {e}")
    
    @staticmethod
    def _clean_timestamp(ts_str: str) -> str:
        """
        Clean timestamp by removing duplicate IST suffixes.
        
        Args:
            ts_str: Timestamp string, possibly with duplicate "IST"
        
        Returns:
            Clean timestamp with single " IST" suffix
        """
        if not ts_str or ts_str == "Never":
            return ts_str
        
        # Remove all " IST" occurrences first
        clean = ts_str.replace(" IST", "").strip()
        
        # Add single " IST" at end
        return f"{clean} IST"
    
    @staticmethod
    def get_status(refresh_type: str) -> Dict[str, Any]:
        """
        Get refresh status for a data type.
        
        Args:
            refresh_type: "sectors", "etfs", or "comprehensive"
        
        Returns:
            Dict with: last_refresh, status, count, freshness
        """
        DataRefreshTracker._ensure_file_exists()
        
        try:
            with open(TRACKER_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            return {
                "last_refresh": "Never",
                "status": "unknown",
                "count": 0,
                "freshness": "unknown",
            }
        
        result = data.get(refresh_type, {})
        
        # Ensure all required fields exist
        if not result:
            return {
                "last_refresh": "Never",
                "status": "unknown",
                "count": 0,
                "freshness": "unknown",
            }
        
        # Get last_refresh and clean it (remove duplicate IST)
        last_refresh = result.get("last_refresh", "Never")
        last_refresh = DataRefreshTracker._clean_timestamp(last_refresh)
        
        return {
            "last_refresh": last_refresh,
            "status": result.get("status", "unknown"),
            "count": result.get("count", 0),
            "freshness": result.get("freshness", "unknown"),
        }
    
    @staticmethod
    def save_refresh(refresh_type: str, status: str = "success", count: int = 0) -> None:
        """
        Save refresh timestamp for a data type.
        Always uses IST timezone for consistency.
        
        Args:
            refresh_type: "sectors", "etfs", or "comprehensive"
            status: "success" or "failed"
            count: number of records processed
        """
        DataRefreshTracker._ensure_file_exists()
        
        # Get current time in IST (THIS IS THE CRITICAL FIX)
        now_ist = datetime.now(IST)
        # Format: "2025-12-29 22:17 IST" (single IST suffix)
        timestamp_str = now_ist.strftime("%Y-%m-%d %H:%M IST")
        
        # Determine freshness
        freshness = "fresh"  # Just saved, so always fresh
        
        try:
            # Read existing data
            with open(TRACKER_FILE, "r") as f:
                data = json.load(f)
        except Exception:
            data = {}
        
        # Update the specific refresh type
        data[refresh_type] = {
            "last_refresh": timestamp_str,
            "status": status,
            "count": count,
            "freshness": freshness,
        }
        
        # Write back to file
        try:
            with open(TRACKER_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save refresh status: {e}")
    
    @staticmethod
    def get_last_refresh_time_ist(refresh_type: str) -> Optional[datetime]:
        """
        Get the last refresh time as IST datetime object.
        Useful for market hours comparison.
        
        Args:
            refresh_type: "sectors", "etfs", or "comprehensive"
        
        Returns:
            datetime object in IST, or None if never refreshed
        """
        status = DataRefreshTracker.get_status(refresh_type)
        ts_str = status.get("last_refresh", "Never")
        
        if ts_str == "Never":
            return None
        
        try:
            # Parse IST timestamp back to datetime
            # Remove " IST" suffix for parsing
            ts_str_clean = ts_str.replace(" IST", "").strip()
            # Parse as naive datetime
            dt_naive = datetime.strptime(ts_str_clean, "%Y-%m-%d %H:%M")
            # Localize to IST
            dt_ist = IST.localize(dt_naive)
            return dt_ist
        except Exception as e:
            print(f"Error parsing timestamp '{ts_str}': {e}")
            return None
    
    @staticmethod
    def get_age_minutes(refresh_type: str) -> int:
        """
        Get age of refresh data in minutes.
        
        Args:
            refresh_type: "sectors", "etfs", or "comprehensive"
        
        Returns:
            Age in minutes, or -1 if never refreshed
        """
        last_time = DataRefreshTracker.get_last_refresh_time_ist(refresh_type)
        
        if last_time is None:
            return -1
        
        now = datetime.now(IST)
        age = now - last_time
        
        return int(age.total_seconds() / 60)
    
    @staticmethod
    def update_status(refresh_type: str, status: str = "success", count: int = 0) -> None:
        """
        Alias for save_refresh() for backward compatibility.
        
        Args:
            refresh_type: "sectors", "etfs", or "comprehensive"
            status: "success" or "failed"
            count: number of records processed
        """
        DataRefreshTracker.save_refresh(refresh_type, status, count)
