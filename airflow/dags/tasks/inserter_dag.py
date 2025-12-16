from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.inserter import run_all as insert_all

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 12, 6),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "postgres_inserter",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["finance", "insert"],
) as dag:

    insert_task = PythonOperator(
        task_id="insert_parquet_to_db",
        python_callable=insert_all
    )
