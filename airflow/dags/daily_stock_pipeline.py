# airflow/dags/daily_stock_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from tasks.downloader_dag import run_all

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='daily_stock_pipeline',
    default_args=default_args,
    description='Daily download and insert stock data',
    schedule_interval='@daily',
    start_date=datetime(2025, 12, 10),
    catchup=False,
) as dag:

    download_task = PythonOperator(
        task_id='download_stock_data',
        python_callable=run_all
    )
