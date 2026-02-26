# airflow/dags/tasks/inserter_tasks.py
from airflow.decorators import task
from datetime import timedelta
from database.insert import insert_interval


@task(
    retries=3,
    retry_delay=timedelta(minutes=5),
)
def insert_interval_task(interval: str) -> None:
    """
    Airflow task wrapper for inserting all parquet files
    of a given interval into Postgres.
    """
    insert_interval(interval)

