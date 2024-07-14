
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator

import logging
import json

from datetime import datetime, timedelta

# def list_keys():
#     bucket= 'raw'
#     hook = S3Hook(aws_conn_id = 'minio_s3_conn')

#     readKey = hook.read_key(key = 'address/address.csv', bucket_name = bucket)#
#     print(readKey)

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email":"anishmachamasi2262@gmail.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG("forex_data_pipeline", start_date=datetime(2023, 11, 19), default_args=default_args, schedule=None)


# Running Spark Job to process the data
forex_processing = SparkSubmitOperator(
    task_id="forex_processing",
    conn_id="spark_conn",
    application="/opt/airflow/dags/scripts/test.py",
    verbose=False,
    dag=dag 
)

# saving_rates = BashOperator(
#     task_id = "saving_rates",
#     bash_command = 'dbt run --project-dir /opt/airflow/dbt/dbttrino/ --profiles-dir /opt/airflow/dbt/',
#     dag=dag,
# )