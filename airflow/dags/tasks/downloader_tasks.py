# airflow/dags/tasks/dowenloader_dags.py
from pathlib import Path
from datetime import timedelta
from airflow.decorators import task
from config.base_config import RAW_DATA_DIR
from database.downloader import download_one
from typing import Optional

@task(
        retries=3,
        retry_delay=timedelta(minutes=5),
    )
def download_stocks_task(symbol: str, interval: str) -> Optional[str]:
    """Airflow task wrapper around download_one.
    Downloads stock data for a given symbol and interval, 
    saving to RAW_DATA_DIR"""
    out_dir = Path(RAW_DATA_DIR) / interval
    result_path = download_one(
        symbol=symbol,
        interval=interval,
        out_dir=out_dir,
    )
# Return path as string (XCom-safe)
    return str(result_path) if result_path else None