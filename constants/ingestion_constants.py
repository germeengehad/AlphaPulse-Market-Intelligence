"""
This file stores all global, unchanging constants.
Used across downloader, database, and training modules.
"""

# ============================================================
# 🟦 Project Settings
# ============================================================

START_DATE = "2010-01-01"

# Market symbols to download
TICKERS = [
    "^GSPC", "^IXIC", "^DJI", "^VIX",
    "GC=F", "CL=F",
    "EURUSD=X", "GBPUSD=X",
    "BTC-USD", "ETH-USD",
    "^TNX",
]

# Download intervals
INTERVALS = ["1d", "1h", "15m"]

# Request pacing and chunk size
SLEEP_BETWEEN = 0.8
CHUNKSIZE = 1000

# Lookback settings (used by downloader)
LOOKBACK = {
    "1d": "max",   # full history
    "1h": "2y",    # last 2 years
    "15m": "60d"   # last 60 days
}

