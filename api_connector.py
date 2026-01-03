# api_connector.py

"""
AngelOne API Connector Module
Handles all communication with AngelOne SmartAPI for live market data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from SmartApi import SmartConnect
import pyotp

class AngelOneConnector:
    """Connect and fetch live market data from AngelOne broker"""

    def __init__(self, apikey, clientcode, password, totpsecret):
        """Initialize with broker credentials"""
        self.apikey = apikey
        self.clientcode = clientcode
        self.password = password
        self.totpsecret = totpsecret
        self.smartapi = None

    def connect(self):
        """Connect to AngelOne API"""
        try:
            # FIXED: Use api_key (with underscore), not apikey
            self.smartapi = SmartConnect(api_key=self.apikey)
            
            totp_code = pyotp.TOTP(self.totpsecret).now()
            session_data = self.smartapi.generateSession(
                self.clientcode,
                self.password,
                totp_code
            )

            if session_data.get("status"):
                return True, "Connected to AngelOne"
            else:
                msg = session_data.get("message", "Login failed")
                return False, f"Login failed: {msg}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def get_historical_df(self, token, daysback=400):
        """Fetch historical daily candles"""
        try:
            todate = datetime.now()
            fromdate = todate - timedelta(days=daysback)
            
            params = {
                "exchange": "NSE",
                "symboltoken": str(token),
                "interval": "ONE_DAY",
                "fromdate": fromdate.strftime("%Y-%m-%d %H:%M"),
                "todate": todate.strftime("%Y-%m-%d %H:%M"),
            }

            data = self.smartapi.getCandleData(params)
            
            if data and data.get("status") and data.get("data"):
                df = pd.DataFrame(
                    data["data"],
                    columns=["timestamp", "open", "high", "low", "close", "volume"]
                )

                df["timestamp"] = pd.to_datetime(df["timestamp"])
                df["close"] = df["close"].astype(float)
                return df.sort_values("timestamp").reset_index(drop=True)
            
            return None
        except Exception:
            return None
