# cint_db.py
from sqlalchemy.engine.create import create_engine
from sqlalchemy.sql.expression import text
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config.base_config import (
    DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME,
)

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("int_db")


def create_database_if_needed():
    admin_url = (
        "postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/postgres"
    )

    engine = create_engine(admin_url)
    conn = engine.raw_connection()

    try:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname=%s",
            (DB_NAME,),
        )

        if not cur.fetchone():
            logger.info("Creating database %s", DB_NAME)
            cur.execute(f"CREATE DATABASE {DB_NAME}")
        else:
            logger.info(
                "Database %s already exists", DB_NAME
            )

        cur.close()

    finally:
        conn.close()
        engine.dispose()


def create_tables_and_indexes():
    db_url = (
        "postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(db_url)

    tables = ["market_1d", "market_1h", "market_15m"]

    with engine.begin() as conn:
        for table in tables:
            conn.execute(
                text(
                    f"""
                    CREATE TABLE IF NOT EXISTS {table} (
                        ts TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                        symbol TEXT NOT NULL,
                        interval TEXT,
                        open DOUBLE PRECISION,
                        high DOUBLE PRECISION,
                        low DOUBLE PRECISION,
                        close DOUBLE PRECISION,
                        adj_close DOUBLE PRECISION,
                        volume BIGINT
                    );
                    """
                )
            )

            rename_pairs = [
                ('"Open"', "open"),
                ('"High"', "high"),
                ('"Low"', "low"),
                ('"Close"', "close"),
                ('"Adj Close"', "adj_close"),
                ('"Adj_Close"', "adj_close"),
                ('"AdjClose"', "adj_close"),
                ('"Volume"', "volume"),
            ]

            for quoted, lower in rename_pairs:
                do_sql = f"""
                DO $$
                BEGIN
                    BEGIN
                        EXECUTE 'ALTER TABLE {table} '
                                'RENAME COLUMN {quoted} TO {lower}';
                    EXCEPTION
                        WHEN undefined_column THEN NULL;
                    END;
                END
                $$;
                """
                conn.execute(text(do_sql))

            dedupe_sql = f"""
            WITH duplicates AS (
                SELECT ctid FROM (
                    SELECT ctid,
                           ROW_NUMBER() OVER (
                               PARTITION BY symbol, ts
                               ORDER BY ctid
                           ) AS rn
                    FROM {table}
                ) t
                WHERE rn > 1
            )
            DELETE FROM {table}
            WHERE ctid IN (SELECT ctid FROM duplicates);
            """
            conn.execute(text(dedupe_sql))

            conn.execute(
                text(
                    f"CREATE INDEX IF NOT EXISTS "
                    f"idx_{table}_ts ON {table} (ts);"
                )
            )

            conn.execute(
                text(
                    f"CREATE UNIQUE INDEX IF NOT EXISTS "
                    f"uq_{table}_symbol_ts ON {table} (symbol, ts);"
                )
            )

    engine.dispose()
    logger.info("Tables and indexes created/ensured.")


if __name__ == "__main__":
    create_database_if_needed()
    create_tables_and_indexes()
