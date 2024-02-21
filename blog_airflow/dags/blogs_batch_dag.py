import datetime
from datetime import timedelta
from pathlib import Path

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator

default_args = {"retry_delay": timedelta(minutes=5), "email_on_failure": False, "email_on_retry": False, "retries": 1}

dag = DAG(
    dag_id="blogs_batch_load",
    start_date=datetime.datetime(2024, 2, 6),
    schedule=None,
    default_args=default_args,
)

files = ["blogs.csv", "comments.csv", "favorites.csv", "opinions.csv", "blog_tags.csv", "tags.csv", "users.csv"]

for file_name in files:
    name = file_name.split(".csv")[0]

    extract_sftp = SFTPOperator(
        task_id=f"download_{name}_file",
        dag=dag,
        operation="get",
        ssh_conn_id="INBOUND_SFTP",
        local_filepath=f"/home/airflow/shared/{file_name}",
        remote_filepath=f"/upload/{file_name}",
    )

    load_stage_table = PostgresOperator(
        task_id=f"load_{name}_stage_table",
        dag=dag,
        postgres_conn_id="DATAWAREHOUSE",
        sql="./sql/stage_load.sql",
        params={
            "table_name": f"staging.stg_{name}",
            "csv_file_path": f"/shared/{file_name}",
        },
    )

    if name not in ["blog_tags", "blogs"]:
        spark_job_params = {
            "num_executors": 1,
            "executor_cores": 1,
            "executor_memory": "1g",
            "total_executor_cores": 1,
            "driver_memory": "1g",
        }
        load_gold_table = SparkSubmitOperator(
            task_id=f"load_{name}_gold_table",
            conn_id="SPARK",
            application=f"{str(Path(__file__).parent)}/spark/dist/main.py",
            py_files=f"{str(Path(__file__).parent)}/spark/dist/jobs.zip",
            jars=f"{str(Path(__file__).parent)}/jars/drivers/postgresql-42.7.1.jar",
            num_executors=spark_job_params["num_executors"],
            executor_cores=spark_job_params["executor_cores"],
            executor_memory=spark_job_params["executor_memory"],
            total_executor_cores=spark_job_params["total_executor_cores"],
            driver_memory=spark_job_params["driver_memory"],
            application_args=[
                "--job",
                f"load_{name}",
                "--jobtype",
                "batch",
            ],
        )
        chain(extract_sftp, load_stage_table, load_gold_table)
    else:
        chain(extract_sftp, load_stage_table)
