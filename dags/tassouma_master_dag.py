from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'yacouba',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'tassouma_full_pipeline',
    default_args=default_args,
    description='Pipeline End-to-End Tassouma: MySQL -> MinIO -> Postgres -> dbt',
    schedule_interval='@daily', 
    catchup=False
) as dag:

    # 1. Extraction MySQL -> MinIO (Bronze Layer - Landing)
    ingest = BashOperator(
        task_id='ingest_mysql_to_minio',
        bash_command='python /usr/app/ingestion_tassouma.py'
    )

    # 2. Chargement MinIO -> Postgres (Bronze Layer - SQL)
    load = BashOperator(
        task_id='load_minio_to_warehouse',
        bash_command='python /usr/app/lake_to_warehouse.py'
    )

    # 3. Transformation dbt (Silver & Gold Layers)
    # Correction des permissions : on redirige les logs et la compilation vers /tmp
    dbt_command = """
    export DBT_LOG_PATH=/tmp/dbt_logs
    export DBT_TARGET_PATH=/tmp/dbt_target
    mkdir -p /tmp/dbt_logs /tmp/dbt_target
    cd /usr/app/tassouma_dbt && dbt run --profiles-dir .
    """

    transform = BashOperator(
        task_id='dbt_transform',
        bash_command=dbt_command
    )

    # L'enchaînement logique du pipeline
    ingest >> load >> transform