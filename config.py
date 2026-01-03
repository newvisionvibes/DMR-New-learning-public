"""
Configuration Module
Centralized configuration for sectors, ETFs, UI, audit, and refresh logic
SAFE VERSION – backward compatible with entire codebase
"""

DATABASE_URL = "postgresql://user:password@host:port/dbname"  # from Fly.io


# ============================================================================
# SECTOR CONFIGURATION
# ============================================================================

SECTOR_TOKENS = {
    "Nifty Auto": {"token": 99926029, "name": "Auto"},
    "NIFTY Bank": {"token": 99926009, "name": "Bank"},
    "NIFTY FMCG": {"token": 99926021, "name": "FMCG"},
    "NIFTY IT": {"token": 99926008, "name": "IT"},
    "NIFTY 50": {"token": 99926000, "name": "Nifty 50"},
    "NIFTY FIN SERVICE": {"token": 99926037, "name": "Financial Services"},
    "NIFTY Next 50": {"token": 99926013, "name": "Next 50"},
    "NIFTY Midcap 50": {"token": 99926014, "name": "Mid 50"},
    "NIFTY MEDIA": {"token": 99926031, "name": "Media"},
    "NIFTY METAL": {"token": 99926030, "name": "Metal"},
    "NIFTY PHARMA": {"token": 99926023, "name": "Pharma"},
    "NIFTY PSU BANK": {"token": 99926025, "name": "PSU Bank"},
    "NIFTY PVT BANK": {"token": 99926047, "name": "Private Bank"},
    "NIFTY REALTY": {"token": 99926018, "name": "Realty"},
    "NIFTY ENERGY": {"token": 99926020, "name": "Energy"},
    "NIFTY INFRA": {"token": 99926019, "name": "Infrastructure"},
    "NIFTY COMMODITIES": {"token": 99926035, "name": "Commodities"},
    "NIFTY CONSUMPTION": {"token": 99926036, "name": "Consumption"},
    "NIFTY CPSE": {"token": 99926041, "name": "CPSE"},
    "NIFTY OIL AND GAS": {"token": 99919051, "name": "Oil & Gas"},
    "NIFTY HEALTHCARE": {"token": 99919011, "name": "Healthcare"},
    "NIFTY CONSR DURBL": {"token": 99919008, "name": "Consumer Durables"},
}

# ============================================================================
# BENCHMARK CONFIGURATION
# ============================================================================

BENCHMARK_TOKENS = {
    "NIFTY 50": {"token": 99926000, "name": "NIFTY 50"},
    "NIFTY BANK": {"token": 99926009, "name": "NIFTY BANK"},
    "NIFTY 500": {"token": 99926004, "name": "NIFTY 500"},
}

# ============================================================================
# RS PERIOD CONFIGURATION
# ============================================================================

RS_PERIODS = {
    "short": 21,
    "medium": 55,
    "long": 123,
}

DEFAULT_RS_PERIODS = [21, 55, 123]

# ============================================================================
# DATA FETCH CONFIGURATION
# ============================================================================

DEFAULT_DAYSBACK = 400
RATE_LIMIT_DELAY = 0.2

# ============================================================================
# OPTION-A DATA REFRESH CONFIGURATION
# ============================================================================

ETF_REFRESH_INTERVAL_MINUTES = 2
SECTOR_REFRESH_INTERVAL_MINUTES = 2

# NSE Market Hours (IST)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 15
MARKET_CLOSE_HOUR = 15
MARKET_CLOSE_MINUTE = 30

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================

SMTP_SERVER_DEFAULT = "smtp.gmail.com"
SMTP_PORT_DEFAULT = 587

# ============================================================================
# AUDIT / LOGGING CONFIGURATION
# ============================================================================

AUDIT_LOGS_FOLDER = "audit_logs"
AUDIT_FILENAME_TEMPLATE = "audit_logs/sector_rs_{benchmark}_{timestamp}.csv"

# ============================================================================
# UI CONFIGURATION
# ============================================================================

METRIC_BOX_WIDTH = 150
METRIC_BOX_MIN_WIDTH = 150

PAGE_CONFIG = {
    "page_title": "Sector & ETF RS Analyzer",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ============================================================================
# TAB NAMES (USED BY main.py)
# ============================================================================

TAB_NAMES = [
    "Home",  
    "Sectors",
    "ETFs RS",
    "Validation",
    "Email",
    "README",
]

# ============================================================================
# CATEGORY COLORS
# ============================================================================

CATEGORY_COLORS = {
    "Outperforming": "🟢",
    "Mixed": "🟡",
    "Underperforming": "🔴",
}
# Existing imports and config...

# -------------------------------------------------------------------
# DATABASE CONFIG (Fly.io Postgres)
# -------------------------------------------------------------------
# Prefer environment variable in production; this is only a fallback.

DATABASE_URL = "postgresql://postgres:Indian@localhost:5432/etf_rs_app"

# -------------------------------------------------------------------
# PAYMENTS / CASHFREE (to be used later)
# -------------------------------------------------------------------
CASHFREE_APP_ID = "your_cashfree_app_id"
CASHFREE_SECRET_KEY = "your_cashfree_secret"
CASHFREE_BASE_URL = "https://sandbox.cashfree.com/pg"  # or live URL
CASHFREE_PLAN_ID_BASIC = "plan_basic"

# -------------------------------------------------------------------
# EMAIL (SES / Brevo) (to be used later)
# -------------------------------------------------------------------
EMAIL_PROVIDER = "ses"  # or "brevo"
EMAIL_FROM = "no-reply@example.com"
AWS_REGION = "ap-south-1"  # for SES
BREVO_API_KEY = "your_brevo_key"
