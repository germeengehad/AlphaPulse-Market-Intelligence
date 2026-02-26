from datetime import datetime, timedelta
from airflow.decorators import dag, task
from constants.ingestion_constants import TICKERS, INTERVALS
from tasks.downloader_tasks import download_stocks_task
from tasks.inserter_tasks import insert_interval_task
from database.insert import create_tables_if_not_exists

@dag(
    dag_id="daily_stock_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["stocks", "ingestion", "yfinance"],
)
def daily_stock_pipeline():
    """
    Orchestrates:
    - Create necessary tables if they don't exist
    - Download stock data
    - Insert into Postgres
    """

    for interval in INTERVALS:

        # 0️⃣ create tables task
        @task(
            task_id=f"create_tables_{interval}",
            retries=1,
            retry_delay=timedelta(minutes=2),
        )
        def create_tables_task(interval: str):
            create_tables_if_not_exists(interval)

        create_tables = create_tables_task(interval)

        # 1️⃣ download tasks (fan-out)
        downloads = [
            download_stocks_task(
                symbol=symbol,
                interval=interval
            )
            for symbol in TICKERS
        ]

        # 2️⃣ insert task (fan-in)
        insert = insert_interval_task(interval)

        # chaining: create_tables -> downloads -> insert
        create_tables >> downloads >> insert


dag = daily_stock_pipeline()