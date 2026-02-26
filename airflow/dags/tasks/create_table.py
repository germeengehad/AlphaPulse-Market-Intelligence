from database.connection import get_engine
from sqlalchemy import text
from tasks.inserter_tasks import insert_interval
from constants.ingestion_constants import INTERVALS

# 1️⃣ Connect to Postgres
engine = get_engine()

# 2️⃣ SQL for creating tables if they do not exist
create_table_sql = {
    "1d": """
    CREATE TABLE IF NOT EXISTS market_1d (
        ts TIMESTAMP NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        adj_close FLOAT,
        volume BIGINT,
        symbol TEXT NOT NULL,
        interval TEXT,
        PRIMARY KEY (symbol, ts)
    );
    """,
    "1h": """
    CREATE TABLE IF NOT EXISTS market_1h (
        ts TIMESTAMP NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        adj_close FLOAT,
        volume BIGINT,
        symbol TEXT NOT NULL,
        interval TEXT,
        PRIMARY KEY (symbol, ts)
    );
    """,
    "15m": """
    CREATE TABLE IF NOT EXISTS market_15m (
        ts TIMESTAMP NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        adj_close FLOAT,
        volume BIGINT,
        symbol TEXT NOT NULL,
        interval TEXT,
        PRIMARY KEY (symbol, ts)
    );
    """,
}

# 3️⃣ Execute table creation
with engine.connect() as conn:
    for interval, sql in create_table_sql.items():
        conn.execute(text(sql))
        print(f"✅ Table for {interval} ensured")

# 4️⃣ Optional: Insert parquet data for all intervals
for interval in INTERVALS:
    insert_interval(interval)
    print(f"📥 Data inserted for {interval}")