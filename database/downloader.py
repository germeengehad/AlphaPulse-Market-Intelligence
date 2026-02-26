# downloader.py
import time
from pathlib import Path
from datetime import datetime
import yfinance as yf
import pandas as pd

from constants.ingestion_constants import (
    TICKERS,
    INTERVALS,
    START_DATE,
    SLEEP_BETWEEN,
    LOOKBACK,
)
from config.base_config import RAW_DATA_DIR, logger
from utils.base_utils import ensure_dir
from utils.ingestion_utils import flatten_columns, sanitize_filename


# ---------------------------------------------
# Yahoo Finance intraday hard limits (days)
# ---------------------------------------------
YAHOO_LIMITS = {
    "1m": 60,
    "2m": 60,
    "5m": 60,
    "15m": 60,
    "30m": 60,
    "60m": 730,
    "1h": 730,
}


def _calculate_start_date(interval: str) -> str:
    """
    Calculate start date based on LOOKBACK and enforce Yahoo limits.
    Returns formatted string YYYY-MM-DD.
    """

    period = LOOKBACK.get(interval)

    if period is None:
        raise ValueError(f"LOOKBACK for interval '{interval}' is missing.")

    # If max history requested
    if period == "max":
        start_ts = pd.Timestamp(START_DATE)

    else:
        if "y" in period:
            years = int(period.replace("y", ""))
            days = years * 365
        elif "d" in period:
            days = int(period.replace("d", ""))
        else:
            raise ValueError(f"Unsupported LOOKBACK format: {period}")

        start_ts = pd.Timestamp.utcnow() - pd.Timedelta(days=days)

    # -----------------------------------------
    # Enforce Yahoo intraday limits
    # -----------------------------------------
    if interval in YAHOO_LIMITS:
        limit_days = YAHOO_LIMITS[interval]
        limit_start = pd.Timestamp.utcnow() - pd.Timedelta(days=limit_days)

        if start_ts < limit_start:
            logger.warning(
                "Start date for %s adjusted to Yahoo limit (%s days).",
                interval,
                limit_days,
            )
            start_ts = limit_start

    return start_ts.strftime("%Y-%m-%d")


def download_one(symbol: str, interval: str, out_dir: Path):
    """
    Download one ticker for a given interval and save as parquet.
    """

    logger.info("Downloading %s @ %s", symbol, interval)

    try:
        # 1m must use period instead of start
        if interval == "1m":
            kwargs = {
                "period": "60d",
                "interval": "1m",
                "progress": False,
                "threads": False,
            }
        else:
            start_date = _calculate_start_date(interval)

            kwargs = {
                "start": start_date,
                "end": pd.Timestamp.utcnow().strftime("%Y-%m-%d"),
                "interval": interval,
                "progress": False,
                "threads": False,
            }

        raw = yf.download(symbol, **kwargs)

        if raw is None or raw.empty:
            logger.warning("No data returned for %s @ %s", symbol, interval)
            return None

        df = raw.reset_index()
        df = flatten_columns(df)

        # Normalize timestamp column
        ts_col = (
            "Date"
            if "Date" in df.columns
            else "Datetime"
            if "Datetime" in df.columns
            else df.columns[0]
        )

        df.rename(columns={ts_col: "ts"}, inplace=True)
        df["ts"] = pd.to_datetime(df["ts"], utc=True)
        df["symbol"] = symbol
        df["interval"] = interval

        ensure_dir(str(out_dir))
        path = out_dir / f"{sanitize_filename(symbol)}.parquet"

        df.to_parquet(path, index=False)

        logger.info("Saved %s rows to %s", len(df), path)
        return path

    except Exception as e:
        logger.exception("Failed downloading %s @ %s: %s", symbol, interval, e)
        return None


def run_all():
    """
    Download all tickers for all intervals.
    Safe for Airflow execution.
    """

    base = Path(RAW_DATA_DIR)

    for interval in INTERVALS:
        interval_dir = base / interval
        ensure_dir(str(interval_dir))

        for symbol in TICKERS:
            download_one(symbol, interval, interval_dir)
            time.sleep(SLEEP_BETWEEN)


if __name__ == "__main__":
    run_all()