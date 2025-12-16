# downloader.py
import time
from pathlib import Path
import yfinance as yf
import pandas as pd
from constants.ingestion_constants import (
    TICKERS,
    INTERVALS,
    START_DATE,
    SLEEP_BETWEEN,
    LOOKBACK,
)
from config.base_config import RAW_DATA_DIR, logger  # use centralized logger
from utils.base_utils import ensure_dir
from utils.ingestion_utils import flatten_columns, sanitize_filename


def download_one(symbol: str, interval: str, out_dir: Path):
    """Download one ticker for a given interval and save as parquet."""
    logger.info("Downloading %s @ %s", symbol, interval)

    # Determine start date / period
    kwargs = {}
    if interval == "1m":
        kwargs = {
            "period": "60d",
            "interval": "1m",
            "progress": False,
            "threads": False,
        }
    else:
        period_days = LOOKBACK.get(interval)
        if period_days == "max":
            kwargs = {
                "start": START_DATE,
                "interval": interval,
                "progress": False,
                "threads": False,
            }
        else:
            # type: ignore
            if period_days is not None and "y" in period_days:
                days = int(period_days.replace("y", "")) * 365
            elif period_days is not None:
                days = int(period_days.replace("d", ""))
            else:
                raise ValueError(
                    f"LOOKBACK for interval '{interval}' is None or invalid."
                )
            start_time = pd.Timestamp.utcnow() - pd.Timedelta(days=days)
            start_ts = start_time.strftime("%Y-%m-%d")
            kwargs = {
                "start": start_ts,
                "interval": interval,
                "progress": False,
                "threads": False,
            }

    # Download data
    raw = yf.download(symbol, **kwargs)
    if raw is None or raw.empty:
        logger.warning("No data for %s @ %s", symbol, interval)
        return None

    df = raw.reset_index()
    df = flatten_columns(df)

    # Normalize timestamp
    ts_col = (
        "Date" if "Date" in df.columns
        else "Datetime" if "Datetime" in df.columns
        else df.columns[0]
    )
    df.rename(columns={ts_col: "ts"}, inplace=True)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    df["symbol"] = symbol
    df["interval"] = interval

    # Write parquet
    ensure_dir(str(out_dir))
    path = out_dir / f"{sanitize_filename(symbol)}.parquet"
    df.to_parquet(path, index=False)
    logger.info("Saved %s rows to %s", len(df), path)
    return path


def run_all():
    """Download all tickers for all intervals."""
    base = Path(RAW_DATA_DIR)
    for interval in INTERVALS:
        interval_dir = base / interval
        ensure_dir(str(interval_dir))
        for symbol in TICKERS:
            try:
                download_one(symbol, interval, interval_dir)
            except Exception as e:
                logger.exception("Failed %s %s: %s", symbol, interval, e)
            time.sleep(SLEEP_BETWEEN)


if __name__ == "__main__":
    run_all()
