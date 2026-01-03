# rs_analyzer.py
"""
Relative Strength Analyzer Module
Calculates RS values and analyzes sector/ETF performance
"""

import pandas as pd
import numpy as np
from datetime import datetime
import time


class SectorRSAnalyzer:
    """Analyze sector relative strength vs benchmark"""

    def __init__(self, connector, sector_tokens):
        """
        Initialize analyzer

        Args:
            connector: AngelOneConnector instance
            sector_tokens: Dict of sector tokens
        """
        self.connector = connector
        self.sector_tokens = sector_tokens

    def calculate_rs(self, sector_df, bench_df, period):
        """
        Calculate Relative Strength for given period

        RS = (Sector Return %) - (Benchmark Return %)
        """
        if sector_df is None or bench_df is None:
            return None

        if len(sector_df) < period or len(bench_df) < period:
            return None

        # Calculate returns
        sector_ret = (
            (sector_df["close"].iloc[-1] - sector_df["close"].iloc[-period - 1])
            / sector_df["close"].iloc[-period - 1]
            * 100
        )
        bench_ret = (
            (bench_df["close"].iloc[-1] - bench_df["close"].iloc[-period - 1])
            / bench_df["close"].iloc[-period - 1]
            * 100
        )

        return round(sector_ret - bench_ret, 2)

    def get_tldr(self, rs1, rs2, rs3, category):
        """Generate TLDR summary based on RS values"""
        if category == "Outperforming":
            if rs2 >= 3:
                return "VERY STRONG momentum - Leading market across all timeframes"
            elif rs2 >= 1.5:
                return "STRONG momentum - Consistently outperforming"
            else:
                return "MODERATELY STRONG - Positive across periods"

        elif category == "Underperforming":
            if rs2 <= -3:
                return "VERY WEAK - Significantly lagging market"
            elif rs2 <= -1.5:
                return "WEAK - Underperforming across periods"
            else:
                return "MODERATELY WEAK - Lagging benchmark"

        else:  # Mixed
            if rs1 > 0 and rs2 > 0:
                return "Gaining momentum - Watch for sustained breakout"
            elif rs1 < 0 and rs2 < 0:
                return "Losing momentum - Former strength fading"
            else:
                return "Volatile pattern - Inconsistent performance"

    def analyze(self, benchmark_token, rs_periods, progress_callback=None):
        """
        Analyze all sectors

        Returns DataFrame with sector analysis
        """
        results = []
        max_period = max(rs_periods)

        # Fetch benchmark data once
        bench_df = self.connector.get_historical_df(benchmark_token, max_period + 2)
        if bench_df is None:
            return pd.DataFrame()

        total = len(self.sector_tokens)
        success_count = 0
        failed_sectors = []

        for idx, (symbol, info) in enumerate(self.sector_tokens.items()):
            if progress_callback:
                progress_callback(idx + 1, total, info["name"])

            # Fetch sector data
            sector_df = self.connector.get_historical_df(
                info["token"], max_period + 2
            )
            if sector_df is None:
                failed_sectors.append(info["name"])
                continue

            # Calculate metrics
            ltp = round(sector_df["close"].iloc[-1], 2)
            prev_close = (
                sector_df["close"].iloc[-2] if len(sector_df) > 1 else ltp
            )
            pct_change = round(
                (ltp - prev_close) / prev_close * 100 if prev_close != 0 else 0,
                2,
            )

            # Calculate RS values
            rs_vals = [
                self.calculate_rs(sector_df, bench_df, period)
                for period in rs_periods
            ]

            # Categorize
            pos = sum(1 for rs in rs_vals if rs and rs > 0)
            neg = sum(1 for rs in rs_vals if rs and rs < 0)

            if pos == len(rs_periods):
                category = "Outperforming"
            elif neg == len(rs_periods):
                category = "Underperforming"
            else:
                category = "Mixed"

            tldr = self.get_tldr(
                rs_vals[0] or 0, rs_vals[1] or 0, rs_vals[2] or 0, category
            )

            result_row = {
                "Sector": info["name"],
                "Symbol": symbol,
                "LTP": ltp,
                "Change": pct_change,
                f"RS_{rs_periods[0]}": round(rs_vals[0], 2) if rs_vals[0] else 0,
                f"RS_{rs_periods[1]}": round(rs_vals[1], 2) if rs_vals[1] else 0,
                f"RS_{rs_periods[2]}": round(rs_vals[2], 2) if rs_vals[2] else 0,
                "Category": category,
                "TLDR": tldr,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            results.append(result_row)
            success_count += 1
            time.sleep(0.2)  # rate limiting

        df = pd.DataFrame(results)
        if not df.empty:
            df = df.sort_values(f"RS_{rs_periods[1]}", ascending=False)

        return df
