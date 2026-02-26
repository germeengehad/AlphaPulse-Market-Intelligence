import time
from pathlib import Path
import pandas as pd
from psycopg2.extras import execute_values
from sqlalchemy import text
from .connection import get_engine
from constants.ingestion_constants import INTERVALS, CHUNKSIZE
from config.base_config import RAW_DATA_DIR, logger
from utils.base_utils import ensure_dir

# Table and column mapping
TABLE_MAP = {"1d": "market_1d", "1h": "market_1h", "15m": "market_15m"}
COLUMN_NORMALIZATION = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Adj_Close": "adj_close",
    "AdjClose": "adj_close",
    "Volume": "volume",
    "VOL": "volume",
}

# Required columns for DB
REQUIRED_COLS = [
    "ts", "open", "high", "low", "close", "adj_close",
    "volume", "symbol", "interval"
]

def create_tables_if_not_exists(interval: str) -> None:
    """Create the table for a given interval if it does not exist."""
    table_name = TABLE_MAP[interval]
    logger.info("Ensuring table exists: %s", table_name)

    engine = get_engine()
    raw_conn = engine.raw_connection()
    try:
        cur = raw_conn.cursor()
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ts TIMESTAMP NOT NULL,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            adj_close FLOAT,
            volume FLOAT,
            symbol TEXT NOT NULL,
            interval TEXT,
            PRIMARY KEY (symbol, ts)
        );
        """
        cur.execute(create_sql)
        raw_conn.commit()
        cur.close()
        logger.info("Table %s is ready.", table_name)
    finally:
        raw_conn.close()
        engine.dispose()


def insert_file(interval: str, file_path: Path) -> None:
    """Insert one parquet file into Postgres for a given interval."""
    table_name = TABLE_MAP[interval]
    logger.info("Inserting %s into %s", file_path.name, table_name)

    df = pd.read_parquet(file_path)

    # 1️⃣ Remove symbol suffix from column names
    df.columns = df.columns.str.replace(r"_\^.*", "", regex=True).str.strip()  # remove _^SYMBOL


    # 2️⃣ Normalize column names
    rename_map = {k: v for k, v in COLUMN_NORMALIZATION.items() if k in df.columns and v not in df.columns}
    if rename_map:
        df = df.rename(columns=rename_map)

    # 3️⃣ Lowercase all column names for DB consistency   
    df.columns = [col.lower() for col in df.columns]


    # 4️⃣ Fix timestamps
    df["ts"] = pd.to_datetime(df["ts"], utc=True).dt.tz_localize(None)

    # 5️⃣ Remove duplicates
    df = df.drop_duplicates(subset=["symbol", "ts"])

   # 6️⃣ Ensure all required columns exist
    cols = ["ts", "open", "high", "low", "close", "adj_close", "volume", "symbol", "interval"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    df["interval"] = interval
    insert_df = df[cols]

    if insert_df.empty:
        logger.info("No rows to insert for %s from %s", table_name, file_path.name)
        return

   # 7️⃣ Prepare rows for insertion
    insert_rows = [tuple(None if pd.isna(x) else x for x in row) for row in insert_df.itertuples(index=False, name=None)]

    engine = get_engine()
    raw_conn = engine.raw_connection()
    try:
        cur = raw_conn.cursor()
        sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES %s ON CONFLICT (symbol, ts) DO NOTHING"
        execute_values(cur, sql, insert_rows, template=None, page_size=min(CHUNKSIZE, 500))
        raw_conn.commit()
        cur.close()
        logger.info("Inserted %s rows from %s", len(insert_rows), file_path.name)
    finally:
        raw_conn.close()
        engine.dispose()


def insert_interval(interval: str) -> None:
    """Insert all parquet files for one interval."""
    folder = Path(RAW_DATA_DIR) / interval
    ensure_dir(folder)

    files = sorted(folder.glob("*.parquet"))
    if not files:
        logger.warning("No raw files for interval %s", interval)
        return

    for file_path in files:
        try:
            insert_file(interval, file_path)
        except Exception as e:
            logger.exception("Failed to insert %s %s: %s", file_path.name, interval, e)
        time.sleep(0.1)


def run_all() -> None:
    """Insert all intervals."""
    for interval in INTERVALS:
        insert_interval(interval)