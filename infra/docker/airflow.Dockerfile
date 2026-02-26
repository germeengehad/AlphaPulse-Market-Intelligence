FROM apache/airflow:2.10.3-python3.9

USER root

# Minimal system deps (stable on WSL)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements
COPY requirements/airflow.txt /opt/airflow/requirements.txt

# Install Python deps using official Airflow constraints
RUN pip install --no-cache-dir \
    -r /opt/airflow/requirements.txt \
    --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.10.3/constraints-3.9.txt
